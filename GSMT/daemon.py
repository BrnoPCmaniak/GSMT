"""Deamon classes for GSMT.

:class:`DaemonizeWithXMLRPC`: :class:`Daemonize` with
    :class:`GSMT.xmlrpc_server.VerifyingServer` built-in.
:class:`Daemon`: Deamon operations and :class:`DaemonizeWithXMLRPC` operation.
"""
import logging
import os
import sys

from daemonize import Daemonize

from GSMT.data_groups import Adress, SystemUser
from GSMT.xmlrpc_server import VerifyingServer


def _init_stdout_logger():
    """Return logger for stdout."""
    logger = logging.getLogger("__main__")
    logger.setLevel(logging.DEBUG)

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    stdout.setFormatter(formatter)
    logger.addHandler(stdout)
    return logger


class DaemonizeWithXMLRPC(Daemonize):
    """Daemonize with built-in xmlrpc_server."""

    server = None
    adress = None
    port = None
    log_requests = None
    is_stopping = False

    def __init__(self, adress=None, log_requests=False,
                 **kwargs):
        """Init :class Daemonize: and :class VerifyingServer:.

        :param str adress: Adress of xmlrpc server
        :param int port: Port of xmlrpc server
        :param log_requests`: should be requests listed in logger?
        """
        super(DaemonizeWithXMLRPC, self).__init__(**kwargs)
        if adress is None:
            self.adress = Adress("localhost", 8000)
        else:
            self.adress = adress
        self.log_requests = log_requests
        self.server = VerifyingServer(self, self.adress.as_tupple(),
                                      logRequests=log_requests)

    def exit(self):
        """Override Daemonize.exit to fix ^C exit traceback."""
        self.logger.warn("Stopping daemon.")
        os.remove(self.pid)

    def start_xmlrpc(self):
        """Start XMLRPC Server."""
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()
        except Exception as exception:  # pylint: disable=w0703
            if self.is_stopping:
                return
            else:
                raise exception

    def stop(self):
        """Stop xmlrpc server and call deamonize exit."""
        self.is_stopping = True
        self.server.server_close()
        return True


class Daemon(object):
    """Daemon class of GSMT."""

    pid = None
    path = None
    daemon = None
    debug = False
    config = None

    def __init__(self, path="/etc/GSMT",  # pylint: disable=r0913
                 verbose=False, foreground=False,
                 adress=Adress("localhost", 8000),
                 system_user=SystemUser(None, None)):
        """Init :class:`DaemonizeWithXMLRPC`.

        If path does not exists create it.
        If verbose create logger to stdout.

        :param:`path`: Path for config, db and pidfile.
        :param:`verbose`: Lower log level to DEBUG.
        :param:`foreground`: If True app stays in foreground and redirect
                        the output to stdout.
        :param:`adress`: Port and Adress for XMLRPC.
        :param:`system_user`: User and group for gsmt-daemon.
        """
        os.makedirs(path, exist_ok=True)  # Create dir when not exists
        self.pid = os.path.join(path, "GSMT.pid")
        self.path = path

        logger = _init_stdout_logger() if foreground else None

        self.adress = adress
        self.system_user = system_user

        self.daemonize = DaemonizeWithXMLRPC(
            adress=adress, app="GSMT", pid=self.pid,
            user=self.system_user.user, group=self.system_user.group,
            verbose=verbose, logger=logger, action=self.main,
            foreground=foreground)

    def main(self):
        """Register functions in xmlrpc and run server."""
        self.daemonize.server.register_introspection_functions()
        self.daemonize.server.register_function(self.daemonize.stop)
        self.daemonize.start_xmlrpc()

    def start(self):
        """Shortcut to start the daemon."""
        self.daemonize.start()
