"""Deamon classes for GSMT.

This module contains classes for GSMT deamonization.

Classes::
* :class DaemonizeWithXMLRPC: :: :class Daemonize: with
    :class GSMT.xmlrpc_server.VerifyingServer: built-in.
* :class Daemon: :: Deamon operations and
    :class DaemonizeWithXMLRPC: operation.

Functions::
* :function _init_stdout_logger: :: Initialize and get logger for programm
   stdout.
"""
import logging
import os
import sys
import time

import configparser
from daemonize import Daemonize

from GSMT.data_groups import Adress, SystemUser
from GSMT.servers_library import GAME_SERVERS
from GSMT.tools import mkdir_p


def _init_stdout_logger():
    """Return logger of __main__ for stdout.

    -**parameters**, **types**, **return** and **return types**

       :return: return logger of __main__
       :rtype: logging.Logger
    """
    logger = logging.getLogger("__main__")
    logger.setLevel(logging.DEBUG)

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    stdout.setFormatter(formatter)
    logger.addHandler(stdout)
    return logger


class DaemonizeNoTraceback(Daemonize):
    """Daemonize whihc overrides ^C exit traceback.

    Methods::
    * :function exit: :: Override Deamonize.exit.
    """

    def exit(self):
        """Override Daemonize.exit to fix ^C exit traceback."""
        self.logger.warn("Stopping daemon.")
        os.remove(self.pid)


class Daemon(object):
    """Daemon class of GSMT."""

    pid = None
    path = None
    daemon = None
    debug = False
    servers_path = None
    logger = None
    server_configs = []
    servers = []

    def __init__(self, path="/etc/GSMT",  # pylint: disable=r0913
                 verbose=False, foreground=False,
                 servers_path="/opt/GSMT",
                 adress=Adress("localhost", 8000),
                 system_user=SystemUser(None, None)):
        """Init :class DaemonizeWithXMLRPC:.

        If path does not exists create it.
        If verbose create logger to stdout.

        -**parameters**, **types**, **return** and **return types**

            :param str path: Path for config, db and pidfile.
            :param boolean verbose: Lower log level to DEBUG.
            :param boolean foreground: If True app stays in foreground and
                redirect the output to stdout.
            :param str servers_path: Path to servers default directory
            :param Adress adress: Port and Adress for XMLRPC.
            :param SystemUser system_user: User and group for gsmt-daemon.
        """
        mkdir_p(path)  # Create dir when not exists
        self.pid = os.path.join(path, "GSMT.pid")
        self.path = path
        self.servers_path = servers_path

        self.logger = _init_stdout_logger() if foreground else None

        self.adress = adress
        self.system_user = system_user

        self._init_servers()

        self.daemonize = DaemonizeNoTraceback(
            app="GSMT", pid=self.pid, user=self.system_user.user, group=self.system_user.group,
            verbose=verbose, logger=self.logger, action=self.main, foreground=foreground)

    def main(self):
        """Register run server."""
        for server in self.servers:
            server.start_on_daemon_start()

        # TODO: Replace with flask
        while True:
            pass

    def _init_servers(self):
        """Init configs for gameservers."""
        for fname in os.listdir(self.path):
            if fname.endswith(".ini"):
                fpath = os.path.join(self.path, fname)
                self.logger.debug("Loading config \"%s\"" % fpath)
                config = configparser.ConfigParser()
                config.read(fpath)
                self.server_configs.append((fpath, config))
                self.parse_config(fpath, config)

    def parse_config(self, fname, config):
        """Parse server config."""
        for section in config.sections():
            self.logger.debug("Parse section \"%s\" in file \"%s\"." % (
                section, fname))
            try:
                server_cl = GAME_SERVERS[config[section].get("type", None)]
                name = section
                path = config[section].get("path", os.path.join(
                    self.servers_path, name))
                buffsize = int(config[section].get("buffsize", 100))
                self.servers.append(server_cl(name, self.logger,
                                              config[section], path, buffsize))
            except KeyError:
                self.logger.error(
                    "Failed to parse file \"%s\" section \"%s\"" % (fname,
                                                                    section))
                continue

    def start(self):
        """Shortcut to start the daemon."""
        self.daemonize.start()

    def stop(self):
        """Stop all servers and call deamon to stop."""
        self.logger.info("Stopping servers.")
        for server in self.servers:
            try:
                server.stop()
            except NotImplementedError:
                pass

        self.daemonize.stop()
