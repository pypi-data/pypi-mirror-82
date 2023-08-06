# Filename: db.py
# pylint: disable=locally-disabled
"""
Database utilities.

"""
from datetime import datetime
import functools
import numbers
import ssl
import io
import os
import json
import re
import pytz
import sys
import numpy as np
from collections import defaultdict, OrderedDict, namedtuple
from inspect import Signature, Parameter
from http.cookiejar import CookieJar
from urllib.parse import urlencode, unquote
from urllib.request import (
    Request,
    build_opener,
    urlopen,
    HTTPCookieProcessor,
    HTTPHandler,
)
from urllib.error import URLError, HTTPError
from io import StringIO
from http.client import IncompleteRead

from .tools import cprint
from .time import Timer
from .logger import get_logger

__author__ = "Tamas Gal"
__copyright__ = "Copyright 2016, Tamas Gal and the KM3NeT collaboration."
__credits__ = []
__license__ = "MIT"
__maintainer__ = "Tamas Gal"
__email__ = "tgal@km3net.de"
__status__ = "Development"

log = get_logger(__name__)  # pylint: disable=C0103

UTC_TZ = pytz.timezone("UTC")

# Ignore invalid certificate error
ssl._create_default_https_context = ssl._create_unverified_context

BASE_URL = "https://km3netdbweb.in2p3.fr"


def we_are_in_lyon():
    """Check if we are on a Lyon machine"""
    import socket

    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        return False
    return ip.startswith("134.158.")


def we_are_on_jupyterhub():
    """Check if we are on the JupyterHub machine"""
    import socket

    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        return False
    return ip == socket.gethostbyname("jupyter.km3net.de")


def we_are_on_km3net_gitlab_ci():
    """Check if we are on a GitLab CI runner server"""
    import urllib.request

    external_ip = urllib.request.urlopen("https://ident.me").read().decode("utf8")
    return external_ip == "131.188.161.155"


def read_csv(text, sep="\t"):
    """Create a DataFrame from CSV text"""
    import pandas as pd  # no top level load to make a faster import of db

    return pd.read_csv(StringIO(text), sep="\t")


def make_empty_dataset():
    """Create an empty dataset"""
    import pandas as pd  # no top level load to make a faster import of db

    return pd.DataFrame()


class DBManager(object):
    """A wrapper for the KM3NeT Web DB"""

    def __init__(self, username=None, password=None, url=None, temporary=False):
        "Create database connection"
        self._cookies = []
        self._parameters = None
        self._doms = None
        self._detectors = None
        self._opener = None
        self._temporary = temporary

        self.log = get_logger(self.__class__.__name__)

        from .config import Config

        config = Config()

        if url is not None:
            self._db_url = url
        else:
            self._db_url = config.db_url or BASE_URL

        self._login_url = self._db_url + "/home.htm"

        if not temporary:
            if we_are_in_lyon():
                self.restore_session(
                    "sid=_kmcprod_134.158_lyo7783844001343100343mcprod1223user"
                )
                return
            if we_are_on_jupyterhub():
                self.restore_session(
                    "sid=_jupyter-km3net_131.188.161.143_"
                    "d9fe89a1568a49a5ac03bdf15d93d799"
                )
                return
            if we_are_on_km3net_gitlab_ci():
                self.restore_session(
                    "sid=_gitlab-km3net_131.188.161.155_"
                    "f835d56ca6d946efb38324d59e040761"
                )
                return

        if username is not None and password is not None:
            self.login(username, password)
        elif config.db_session_cookie not in (None, ""):
            self.restore_session(config.db_session_cookie)
        elif all(v in os.environ for v in ["KM3NET_DB_USERNAME", "KM3NET_DB_PASSWORD"]):
            login_ok = self.login(
                os.environ["KM3NET_DB_USERNAME"], os.environ["KM3NET_DB_PASSWORD"]
            )
            if not login_ok:
                self.log.critical("Login failed with credentail from ENV")
                sys.exit(1)
        else:
            username, password = config.db_credentials
            login_ok = self.login(username, password)
            if (
                login_ok
                and not self._temporary
                and input("Request permanent session? (y/n)") in "yY"
            ):
                self.request_permanent_session(username, password)

    def datalog(self, parameter, run, maxrun=None, det_id="D_ARCA001"):
        "Retrieve datalogs for given parameter, run(s) and detector"
        parameter = parameter.lower()
        if maxrun is None:
            maxrun = run
        with Timer("Database lookup"):
            return self._datalog(parameter, run, maxrun, det_id)

    def _datalog(self, parameter, run, maxrun, det_id):
        "Extract data from database"
        values = {
            "parameter_name": parameter,
            "minrun": run,
            "maxrun": maxrun,
            "detid": det_id,
        }
        data = urlencode(values)
        content = self._get_content("streamds/datalognumbers.txt?" + data)
        if content.startswith("ERROR"):
            self.log.error(content)
            return None
        try:
            dataframe = read_csv(content)
        except ValueError:
            self.log.warning("Empty dataset")  # ...probably. Waiting for more info
            return make_empty_dataset()
        else:
            add_datetime(dataframe)
            try:
                self._add_converted_units(dataframe, parameter)
            except KeyError:
                self.log.warning(
                    "Could not add converted units for {0}".format(parameter)
                )
            return dataframe

    def run_table(self, det_id="D_ARCA001"):
        url = "streamds/runs.txt?detid={0}".format(det_id)
        content = self._get_content(url)
        try:
            df = read_csv(content)
        except ValueError:
            self.log.warning("Empty dataset")
            return None
        else:
            timestamp_column = "UNIXSTARTTIME"
            add_datetime(df, timestamp_column)
            df["RUNDURATION"] = -df[timestamp_column].diff(periods=-1) / 1000
            return df

    def _add_converted_units(self, dataframe, parameter, key="VALUE"):
        """Add an additional DATA_VALUE column with converted VALUEs"""
        convert_unit = self.parameters.get_converter(parameter)
        try:
            self.log.debug("Adding unit converted DATA_VALUE to the data")
            dataframe[key] = dataframe["DATA_VALUE"].apply(convert_unit)
        except KeyError:
            self.log.warning("Missing 'VALUE': no unit conversion.")
        else:
            dataframe.unit = self.parameters.unit(parameter)

    @property
    def detectors(self):
        if self._detectors is None:
            self._detectors = self._get_detectors()
        return self._detectors

    def _get_detectors(self):
        content = self._get_content("streamds/detectors.txt")
        try:
            dataframe = read_csv(content)
        except ValueError:
            self.log.warning("Empty dataset")
            return make_empty_dataset()
        else:
            return dataframe

    def get_det_id(self, det_oid):
        """Convert detector string representation (OID) to serialnumber"""
        try:
            return self.detectors[self.detectors.OID == det_oid].SERIALNUMBER.iloc[0]
        except IndexError:
            self.log.critical("No det ID found for OID '{}'".format(det_oid))
            return None

    def get_det_oid(self, det_id):
        """Convert detector serialnumber to string representation (OID)"""
        try:
            return self.detectors[self.detectors.SERIALNUMBER == det_id].OID.iloc[0]
        except IndexError:
            self.log.critical("No OID found for det ID '{}'".format(det_id))
            return None

    def to_det_id(self, det_id_or_det_oid):
        """Convert det ID or OID to det ID"""
        try:
            int(det_id_or_det_oid)
        except ValueError:
            return self.get_det_id(det_id_or_det_oid)
        else:
            return det_id_or_det_oid

    def to_det_oid(self, det_id_or_det_oid):
        """Convert det OID or ID to det OID"""
        try:
            int(det_id_or_det_oid)
        except ValueError:
            return det_id_or_det_oid
        else:
            return self.get_det_oid(det_id_or_det_oid)

    @property
    def parameters(self):
        "Return the parameters container for quick access to their details"
        if self._parameters is None:
            self._load_parameters()
        return self._parameters

    def _load_parameters(self):
        "Retrieve a list of available parameters from the database"
        parameters = self._get_json("allparam/s")
        data = {}
        for parameter in parameters:  # There is a case-chaos in the DB
            data[parameter["Name"].lower()] = parameter
        self._parameters = ParametersContainer(data)

    def trigger_setup(self, runsetup_oid):
        "Retrieve the trigger setup for a given runsetup OID"
        r = self._get_content(
            "jsonds/rslite/s?rs_oid={}&upifilter=1.1.2.2.3/*".format(runsetup_oid)
        )
        data = json.loads(r)["Data"]
        if not data:
            self.log.error("Empty dataset.")
            return
        raw_setup = data[0]
        det_id = raw_setup["DetID"]
        name = raw_setup["Name"]
        description = raw_setup["Desc"]

        _optical_df = raw_setup["ConfGroups"][0]
        optical_df = {"Name": _optical_df["Name"], "Desc": _optical_df["Desc"]}
        for param in _optical_df["Params"]:
            pname = self.parameters.oid2name(param["OID"]).replace("DAQ_", "")
            try:
                dtype = float if "." in param["Val"] else int
                val = dtype(param["Val"])
            except ValueError:
                val = param["Val"]
            optical_df[pname] = val

        if len(raw_setup["ConfGroups"]) > 1:
            _acoustic_df = raw_setup["ConfGroups"][1]
            acoustic_df = {"Name": _acoustic_df["Name"], "Desc": _acoustic_df["Desc"]}
            for param in _acoustic_df["Params"]:
                pname = self.parameters.oid2name(param["OID"]).replace("DAQ_", "")
                try:
                    dtype = float if "." in param["Val"] else int
                    val = dtype(param["Val"])
                except ValueError:
                    val = param["Val"]
                acoustic_df[pname] = val
        else:
            acoustic_df = {"Not available": None}

        return TriggerSetup(
            runsetup_oid, name, det_id, description, optical_df, acoustic_df
        )

    def detx(self, det_id, t0set=None, calibration=None):
        """Retrieve the detector file for given detector id

        If t0set is given, append the calibration data.
        """
        url = "detx/{0}?".format(det_id)  # '?' since it's ignored if no args
        if t0set is not None:
            url += "&t0set=" + t0set
        if calibration is not None:
            url += "&calibrid=" + calibration

        detx = self._get_content(url)
        return detx

    def detx_for_run(self, det_id, run):
        """Retrieve the calibrate detector file for given run"""
        run_table = self.run_table(det_id)
        try:
            run_info = run_table[run_table.RUN == run].iloc[0]
        except IndexError:
            self.log.error("Run {} not found for detector {}".format(run, det_id))
            return None

        tcal = run_info.T0_CALIBSETID
        if str(tcal) == "nan":
            self.log.warning(
                "No time calibration found for run {} (detector {})".format(run, det_id)
            )
            tcal = 0

        try:
            pcal = int(run_info.POS_CALIBSETID)
        except ValueError:
            self.log.warning(
                "No position calibration found for run {} (detector {})".format(
                    run, det_id
                )
            )
            pcal = 0

        try:
            rcal = int(run_info.ROT_CALIBSETID)
        except ValueError:
            self.log.warning(
                "No rotation calibration found for run {} (detector {})".format(
                    run, det_id
                )
            )
            rcal = 0

        url = "detx/{det_id}?tcal={tcal}&pcal={pcal}&rcal={rcal}".format(
            det_id=det_id, tcal=tcal, pcal=pcal, rcal=rcal
        )

        detx = self._get_content(url)
        return detx

    def ahrs(self, run, maxrun=None, clbupi=None, det_id="D_ARCA001"):
        "Retrieve AHRS values for given run(s) (optionally CLBs) and detector"
        if maxrun is None:
            maxrun = run
        with Timer("Database lookup"):
            return self._ahrs(run, maxrun, clbupi, det_id)

    def _ahrs(self, run, maxrun, clbupi, det_id):
        values = {
            "minrun": run,
            "maxrun": maxrun,
            "detid": det_id,
        }
        if clbupi is not None:
            values["clbupi"] = clbupi
        data = urlencode(values)
        content = self._get_content("streamds/ahrs.txt?" + data)
        if content.startswith("ERROR"):
            self.log.error(content)
            return None
        try:
            dataframe = read_csv(content)
        except ValueError:
            self.log.warning("Empty dataset")  # ...probably. Waiting for more info
            return make_empty_dataset()
        else:
            add_datetime(dataframe)
            return dataframe

    def _get_json(self, url):
        "Get JSON-type content"
        content = self._get_content("jsonds/" + url)
        try:
            json_content = json.loads(content.decode())
        except AttributeError:
            json_content = json.loads(content)
        if json_content.get("Comment") is not None:
            self.log.warning(json_content["Comment"])
        if json_content["Result"] != "OK":
            self.log.critical("Error from DB: %s", json_content.get("Data"))
            raise ValueError("Error while retrieving the parameter list.")
        return json_content["Data"]

    def _get_content(self, url):
        "Get HTML content"
        target_url = self._db_url + "/" + unquote(url)  # .encode('utf-8'))
        self.log.debug("Opening '{0}'".format(target_url))
        try:
            f = self.opener.open(target_url)
        except HTTPError as e:
            self.log.error(
                "HTTP error, your session may be expired.\n"
                "Original HTTP error: {}\n"
                "Target URL: {}".format(e, target_url)
            )
            if input("Request new permanent session and retry? (y/n)") in "yY":
                self.request_permanent_session()
                return self._get_content(url)
            else:
                return None
        self.log.debug("Accessing '{0}'".format(target_url))
        try:
            content = f.read()
        except IncompleteRead as icread:
            self.log.critical(
                "Incomplete data received from the DB, "
                + "the data could be corrupted."
            )
            content = icread.partial
        self.log.debug("Got {0} bytes of data.".format(len(content)))
        return content.decode("utf-8")

    @property
    def opener(self):
        "A reusable connection manager"
        if self._opener is None:
            self.log.debug("Creating connection handler")
            opener = build_opener()
            if self._cookies:
                self.log.debug("Appending cookies")
            else:
                self.log.debug("No cookies to append")
            for cookie in self._cookies:
                cookie_str = cookie.name + "=" + cookie.value
                opener.addheaders.append(("Cookie", cookie_str))
            self._opener = opener
        else:
            self.log.debug("Reusing connection manager")
        return self._opener

    def request_sid_cookie(self, username, password):
        """Request cookie for permanent session token."""
        self.log.debug("Requesting SID cookie")
        target_url = self._login_url + "?usr={0}&pwd={1}&persist=y".format(
            username, password
        )
        cookie = urlopen(target_url).read()
        return cookie

    def restore_session(self, cookie):
        """Establish databse connection using permanent session cookie"""
        self.log.debug("Restoring session from cookie: {}".format(cookie))
        opener = build_opener()
        opener.addheaders.append(("Cookie", cookie))
        self._opener = opener

    def request_permanent_session(self, username=None, password=None):
        self.log.debug("Requesting permanent session")

        from .config import Config

        config = Config()

        if username is None and password is None:
            self.log.debug("Checking configuration file for DB credentials")
            username, password = config.db_credentials
        cookie = self.request_sid_cookie(username, password)
        cookie_str = str(cookie, "utf-8")  # Python 3
        self.log.debug("Session cookie: {0}".format(cookie_str))
        self.log.debug("Storing cookie in configuration file")
        config.set("DB", "session_cookie", cookie_str)
        # self._cookies = [cookie]
        self.restore_session(cookie)

    def login(self, username, password):
        "Login to the database and store cookies for upcoming requests."
        self.log.debug("Logging in to the DB")
        opener = self._build_opener()
        values = {"usr": username, "pwd": password}
        req = self._make_request(self._login_url, values)
        try:
            self.log.debug("Sending login request")
            f = opener.open(req)
        except URLError as e:
            self.log.error("Failed to connect to the database -> probably down!")
            self.log.error("Error from database server:\n    {0}".format(e))
            return False
        html = f.read()
        failed_auth_message = "Bad username or password"
        if failed_auth_message in str(html):
            self.log.error(failed_auth_message)
            return False
        return True

    def _build_opener(self):
        self.log.debug("Building opener.")
        cj = CookieJar()
        self._cookies = cj
        opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
        return opener

    def _make_request(self, url, values):
        data = urlencode(values)
        return Request(url, data.encode("utf-8"))

    def _post(self, url, data):
        pass


def add_datetime(dataframe, timestamp_key="UNIXTIME", scale_factor=1e3):
    """Add an additional DATETIME column with standar datetime format.

    This currently manipulates the incoming DataFrame!
    """

    def convert_data(timestamp):
        return datetime.fromtimestamp(float(timestamp) / scale_factor, UTC_TZ)

    try:
        log.debug("Adding DATETIME column to the data")
        converted = dataframe[timestamp_key].apply(convert_data)
        dataframe["DATETIME"] = converted
    except KeyError:
        log.warning("Could not add DATETIME column")


class StreamDS(object):
    """Access to the streamds data stored in the KM3NeT database."""

    def __init__(self, username=None, password=None, url=None, temporary=False):
        self._db = DBManager(username, password, url, temporary)
        self._stream_df = None
        self._streams = None

        self._update_streams()

    def _update_streams(self):
        """Update the list of available straems"""
        content = self._db._get_content("streamds")
        self._stream_df = read_csv(content).sort_values("STREAM")
        self._streams = None
        for stream in self.streams:
            setattr(self, stream, self.__getattr__(stream))

    def __getattr__(self, attr):
        """Magic getter which optionally populates the function signatures"""
        if attr in self.streams:
            stream = attr
        else:
            raise AttributeError

        def func(**kwargs):
            return self.get(stream, **kwargs)

        func.__doc__ = self._stream_parameter(stream, "DESCRIPTION")

        sig_dict = OrderedDict()
        for sel in self.mandatory_selectors(stream):
            if sel == "-":
                continue
            sig_dict[Parameter(sel, Parameter.POSITIONAL_OR_KEYWORD)] = None
        for sel in self.optional_selectors(stream):
            if sel == "-":
                continue
            sig_dict[Parameter(sel, Parameter.KEYWORD_ONLY)] = None
        func.__signature__ = Signature(parameters=sig_dict)

        return func

    @property
    def streams(self):
        """A list of available streams"""
        if self._streams is None:
            self._streams = list(self._stream_df["STREAM"].values)
        return self._streams

    def _stream_parameter(self, stream, parameter):
        data = self._stream_df[self._stream_df.STREAM == stream]
        if "SELECTORS" in parameter:
            return list(data[parameter].values[0].split(","))
        else:
            return data[parameter].values[0]

    def mandatory_selectors(self, stream):
        """A list of mandatory selectors for a given stream"""
        return self._stream_parameter(stream, "MANDATORY_SELECTORS")

    def optional_selectors(self, stream):
        """A list of optional selectors for a given stream"""
        return self._stream_parameter(stream, "OPTIONAL_SELECTORS")

    def help(self, stream):
        """Show the help for a given stream."""
        if stream not in self.streams:
            log.error("Stream '{}' not found in the database.".format(stream))
        params = self._stream_df[self._stream_df["STREAM"] == stream].values[0]
        self._print_stream_parameters(params)

    def print_streams(self):
        """Print a coloured list of streams and its parameters"""
        for row in self._stream_df.itertuples():
            self._print_stream_parameters(row[1:])

    def _print_stream_parameters(self, values):
        """Print a coloured help for a given tuple of stream parameters."""
        cprint("{0}".format(*values), "magenta", attrs=["bold"])
        print("{4}".format(*values))
        cprint("  available formats:   {1}".format(*values), "blue")
        cprint("  mandatory selectors: {2}".format(*values), "red")
        cprint("  optional selectors:  {3}".format(*values), "green")
        print()

    def get(self, stream, fmt="txt", **kwargs):
        """Get the data for a given stream manually"""
        sel = "".join(["&{0}={1}".format(k, v) for (k, v) in kwargs.items()])
        url = "streamds/{0}.{1}?{2}".format(stream, fmt, sel[1:])
        data = self._db._get_content(url)
        if not data:
            log.error("No data found at URL '%s'." % url)
            return
        if data.startswith("ERROR"):
            log.error(data)
            return
        if fmt == "txt":
            return read_csv(data)
        return data


class ParametersContainer(object):
    """Provides easy access to parameters"""

    def __init__(self, parameters):
        self._parameters = parameters
        self._converters = {}
        self._oid_lookup = defaultdict(lambda: None)

    @property
    def names(self):
        "A list of parameter names"
        return list(self._parameters.keys())

    def get_parameter(self, parameter):
        "Return a dict for given parameter"
        parameter = self._get_parameter_name(parameter)
        return self._parameters[parameter]

    def get_converter(self, parameter):
        """Generate unit conversion function for given parameter"""
        if parameter not in self._converters:
            param = self.get_parameter(parameter)
            try:
                scale = float(param["Scale"])
            except KeyError:
                scale = 1

            def convert(value):
                # easy_scale = float(param['EasyScale'])
                # easy_scale_multiplier = float(param['EasyScaleMultiplier'])
                return value * scale

            return convert

    def unit(self, parameter):
        "Get the unit for given parameter"
        parameter = self._get_parameter_name(parameter).lower()
        return self._parameters[parameter]["Unit"]

    def oid2name(self, oid):
        "Look up the parameter name for a given OID"
        if not self._oid_lookup:
            for name, data in self._parameters.items():
                self._oid_lookup[data["OID"]] = data["Name"]
        return self._oid_lookup[oid]

    def _get_parameter_name(self, name):
        if name in self.names:
            return name

        aliases = [n for n in self.names if n.endswith(" " + name)]
        if len(aliases) == 1:
            log.info("Alias found for {0}: {1}".format(name, aliases[0]))
            return aliases[0]

        log.info("Parameter '{0}' not found, trying to find alternative.".format(name))
        try:
            # ahrs_g[0] for example should be looked up as ahrs_g
            alternative = re.findall(r"(.*)\[[0-9*]\]", name)[0]
            log.info("Found alternative: '{0}'".format(alternative))
            return alternative
        except IndexError:
            raise KeyError("Could not find alternative for '{0}'".format(name))


class DOM(object):
    """Represents a DOM"""

    def __init__(self, clb_upi, dom_id, dom_upi, du, det_oid, floor):
        self.clb_upi = clb_upi
        self.dom_id = dom_id
        self.dom_upi = dom_upi
        self.du = du
        self.det_oid = det_oid
        self.floor = floor

    @classmethod
    def from_json(cls, json):
        return cls(
            json["CLBUPI"],
            json["DOMId"],
            json["DOMUPI"],
            json["DU"],
            json["DetOID"],
            json["Floor"],
        )

    @property
    def omkey(self):
        return (self.du, self.floor)

    def __str__(self):
        return "DU{0}-DOM{1}".format(self.du, self.floor)

    def __repr__(self):
        return (
            "{0} - DOM ID: {1}\n"
            "   DOM UPI: {2}\n"
            "   CLB UPI: {3}\n"
            "   DET OID: {4}\n".format(
                self.__str__(), self.dom_id, self.dom_upi, self.clb_upi, self.det_oid
            )
        )


class TriggerSetup(object):
    def __init__(
        self, runsetup_oid, name, det_id, description, optical_df, acoustic_df
    ):
        self.runsetup_oid = runsetup_oid
        self.name = name
        self.det_id = det_id
        self.description = description
        self.optical_df = optical_df
        self.acoustic_df = acoustic_df

    def __str__(self):
        text = (
            "Runsetup OID: {}\n"
            "Name: {}\n"
            "Detector ID: {}\n"
            "Description:\n    {}\n\n".format(
                self.runsetup_oid, self.name, self.det_id, self.description
            )
        )
        for df, parameters in zip(
            ["Optical", "Acoustic"], [self.optical_df, self.acoustic_df]
        ):
            text += "{} Datafilter:\n".format(df)
            for parameter, value in parameters.items():
                text += "  {}: {}\n".format(parameter, value)
            text += "\n"
        return text

    def __repr__(self):
        return str(self)


@functools.lru_cache()
def clbupi2compassupi(clb_upi):
    """Return Compass UPI from CLB UPI."""
    sds = StreamDS()
    upis = sds.integration(container_upi=clb_upi).CONTENT_UPI.values
    compass_upis = [upi for upi in upis if ("AHRS" in upi) or ("LSM303" in upi)]
    if len(compass_upis) > 1:
        log.warning(
            "Multiple compass UPIs found for CLB UPI {}. "
            "Using the first entry.".format(clb_upi)
        )
    return compass_upis[0]


def clbupi2ahrsupi(clb_upi):
    """Return UPI from CLB UPI. Wrap clbupi2compassupi for back-compatibility."""
    log.deprecation("clbupi2ahrsupi is deprecated ! You should use clbupi2compassupi.")
    upi = clbupi2compassupi(clb_upi)
    if upi.split("/")[1] != "AHRS":
        log.warning("clbupi2ahrsupi() is returning a LSM303 UPI : {}".format(upi))
    return upi


def show_compass_calibration(clb_upi, version="3"):
    """Show compass calibration data for given `clb_upi`."""
    db = DBManager()
    compass_upi = clbupi2compassupi(clb_upi)
    compass_model = compass_upi.split("/")[1]
    print("Compass UPI: {}".format(compass_upi))
    print("Compass model: {}".format(compass_model))
    content = db._get_content(
        "show_product_test.htm?upi={compass_upi}&"
        "testtype={model}-CALIBRATION-v{version}&n=1&out=xml".format(
            compass_upi, compass_model, version
        )
    ).replace("\n", "")

    import xml.etree.ElementTree as ET

    try:
        root = ET.parse(io.StringIO(content)).getroot()
    except ET.ParseError:
        print("No calibration data found")
    else:
        for child in root:
            print("{}: {}".format(child.tag, child.text))
        names = [c.text for c in root.findall(".//Name")]
        values = [[i.text for i in c] for c in root.findall(".//Values")]
        for name, value in zip(names, values):
            print("{}: {}".format(name, value))


def show_ahrs_calibration(clb_upi, version="3"):
    """Show AHRS calibration data for given `clb_upi`."""
    log.deprecation(
        "show_ahrs_calibration is deprecated ! You should use show_compass_calibration()."
    )
    show_compass_calibration(clb_upi, version=version)


class CLBMap(object):
    par_map = {"DETOID": "det_oid", "UPI": "upi", "DOMID": "dom_id"}

    def __init__(self, det_oid):
        self.log = get_logger("CLBMap")
        if isinstance(det_oid, numbers.Integral):
            db = DBManager()
            _det_oid = db.get_det_oid(det_oid)
            if _det_oid is not None:
                det_oid = _det_oid
        self.det_oid = det_oid
        sds = StreamDS()
        self._data = sds.clbmap(detoid=det_oid)
        self._by = {}

    def __len__(self):
        return len(self._data)

    @property
    def upis(self):
        """A dict of CLBs with UPI as key"""
        parameter = "UPI"
        if parameter not in self._by:
            self._populate(by=parameter)
        return self._by[parameter]

    @property
    def dom_ids(self):
        """A dict of CLBs with DOM ID as key"""
        parameter = "DOMID"
        if parameter not in self._by:
            self._populate(by=parameter)
        return self._by[parameter]

    @property
    def omkeys(self):
        """A dict of CLBs with the OMKey tuple (DU, floor) as key"""
        parameter = "omkey"
        if parameter not in self._by:
            self._by[parameter] = {}
            for clb in self.upis.values():
                omkey = (clb.du, clb.floor)
                self._by[parameter][omkey] = clb
            pass
        return self._by[parameter]

    def base(self, du):
        """Return the base CLB for a given DU"""
        parameter = "base"
        if parameter not in self._by:
            self._by[parameter] = {}
            for clb in self.upis.values():
                if clb.floor == 0:
                    self._by[parameter][clb.du] = clb
        return self._by[parameter][du]

    def _populate(self, by):
        data = {}
        for _, row in self._data.iterrows():
            data[row[by]] = CLB(
                det_oid=row["DETOID"],
                floor=row["FLOORID"],
                du=row["DUID"],
                serial_number=row["SERIALNUMBER"],
                upi=row["UPI"],
                dom_id=row["DOMID"],
            )
        self._by[by] = data


CLB = namedtuple("CLB", ["det_oid", "floor", "du", "serial_number", "upi", "dom_id"])
