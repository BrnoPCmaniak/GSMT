"""Deamon classes for GSMT.

:class:`DaemonizeWithXMLRPC`: :class:`Daemonize` with
    :class:`GSMT.xmlrpc_server.VerifyingServer` built-in.
:class:`Daemon`: Deamon operations and :class:`DaemonizeWithXMLRPC` operation.
"""
import logging
import os
import sys

from daemonize import Daemonize

from GSMT.xmlrpc_server import VerifyingServer


class DaemonizeWithXMLRPC(Daemonize):
    """Daemonize with built-in xmlrpc_server."""

    server = None
    adress = None
    port = None
    log_requests = None

    def __init__(self, adress="localhost", port=8000, log_requests=False,
                 **kwargs):
        """Init :class:`Daemonize` and :class:`VerifyingServer`.

        :param:`adress`: Adress of xmlrpc server
        :param:`port`: Port of xmlrpc server
        :param:`log_requests`: should be requests listed in logger?
        """
        super(DaemonizeWithXMLRPC, self).__init__(**kwargs)
        self.adress = adress
        self.port = port
        self.log_requests = log_requests
        self.server = VerifyingServer(self, (adress, port),
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


class Daemon(object):
    """Daemon class of GSMT."""

    pid = None
    daemon = None
    debug = False

    def __init__(self, path="/etc/GSMT", verbose=False, foreground=False,
                 port=8000, adress="localhost", user=None, group=None):
        """Init :class:`DaemonizeWithXMLRPC`.

        If path does not exists create it.
        If debug create logger to stdout.

        :param:`path`: Path for config, db and pidfile.
        :param:`verbose`: Lower log level to DEBUG.
        :param:`foreground`: If True app stays in foreground and redirect
                        the output to stdout.
        :param:`port`: Port for XMLRPC.
        :param:`adress`: Adress for XMLRPC.
        :param:`user`: User for gsmt-daemon.
        :param:`group`: Group for gsmt-daemon.
        """
        os.makedirs(path, exist_ok=True)  # Create dir when not exists
        self.pid = os.path.join(path, "GSM.pid")

        if foreground:
            # if debug create new logger to stdout
            logger = logging.getLogger("__main__")
            logger.setLevel(logging.DEBUG)

            stdout = logging.StreamHandler(sys.stdout)
            stdout.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
            stdout.setFormatter(formatter)
            logger.addHandler(stdout)
        else:
            # otherwise use system logger
            logger = None

        self.daemonize = DaemonizeWithXMLRPC(
            adress=adress, port=port, app="GSMT", pid=self.pid, user=user,
            group=group, action=self.main, foreground=foreground,
            verbose=verbose, logger=logger)

    def main(self):
        """Register functions in xmlrpc and run server."""
        self.daemonize.server.register_introspection_functions()
        self.daemonize.start_xmlrpc()

    def start(self):
        """Shortcut to start the daemon."""
        self.daemonize.start()
