"""Game server classes."""
from collections import deque
from subprocess import PIPE, Popen
from threading import Thread
from time import time

from GSMT.exceptions import ServerNotRunning
from GSMT.tools import mkdir_p, remove_newline


class Server(object):
    # pylint: disable=too-many-instance-attributes
    """Game server class."""

    name = None
    status = False
    returncode = None
    logger = None
    path = None
    config = None
    process = None
    stdout_deque = None
    stdout_watcher_thread = None
    stderr_deque = None
    stderr_watcher_thread = None
    stdin_deque = None
    watchdog_thread = None

    def __init__(self, name, logger, config, path, buffsize=100):
        """Init game_server.

        -**parameters**, **types**, **return** and **return types**

            :param str name: Name of server director and is also used for
             generating default path to the server.
            :param Logger logger: Instance of logger.
            :param ConfigParse config: Instance of section within the config
             parse.
            :param str path: Path to the server directory.
            :param int buffsize: Number of recent lines to be stored.
        """
        self.name = name
        self.logger = logger
        self.config = config
        self.path = path
        self.stdin_deque = deque(maxlen=buffsize)
        self.stdout_deque = deque(maxlen=buffsize)
        self.stderr_deque = deque(maxlen=buffsize)

        mkdir_p(path)

        self.logger.debug("Initialized server \"%s\" on path \"%s\"." % (name, path))

    def start(self):
        """Override this method to call self._start."""
        raise NotImplementedError

    def setup(self):
        """Download and setup server."""
        raise NotImplementedError

    def stop(self):
        """Stop the server."""
        raise NotImplementedError

    def terminate(self):
        """Terminate the server."""
        self.logger.warn("Terminating server %s " % self.name)
        self.process.terminate()

    def kill(self):
        """Terminate the server."""
        self.logger.warn("Killing server %s " % self.name)
        self.process.kill()

    def start_on_daemon_start(self):
        """If server option start_on_deamon_start is true start server."""
        if self.config.getboolean("start_on_daemon_start", fallback=False):
            self.start()

    def _stdout_watcher(self):
        """Watch STDOUT output of self.process."""
        start_msg = "Starting STDOUT watcher for %s" % self.name
        server_name = "[%s] - " % self.name
        self.logger.debug(start_msg)
        self.stdout_deque.append((time(), "GSMT: %s" % start_msg))
        try:
            with self.process.stdout:
                for line in iter(self.process.stdout.readline, ''):
                    self.logger.info(server_name + remove_newline(line))
                    self.stdout_deque.append((time(), remove_newline(line)))
        finally:
            stop_msg = "Stopping STDOUT watcher for %s" % self.name
            self.logger.debug(stop_msg)
            self.stdout_deque.append((time(), "GSMT: %s" % stop_msg))

    def _stderr_watcher(self):
        """Watch STDERR output of self.process."""
        start_msg = "Starting STDERR watcher for %s" % self.name
        server_name = "[%s] - " % self.name
        self.logger.debug(start_msg)
        self.stderr_deque.append((time(), "GSMT: %s" % start_msg))
        try:
            with self.process.stderr:
                for line in iter(self.process.stderr.readline, ''):
                    self.logger.error(server_name + remove_newline(line))
                    self.stderr_deque.append((time(), remove_newline(line)))
        finally:
            stop_msg = "Stopping STDERR watcher for %s" % self.name
            self.logger.debug(stop_msg)
            self.stderr_deque.append((time(), "GSMT: %s" % stop_msg))

    def _watchdog(self):
        """Kepp eye on process and check if it is running.

        Workaround for unreliable process.poll().
        """
        self.status = True
        self.returncode = self.process.wait()
        self.status = False

    def _start(self, command):
        """Abstract start command solution."""
        self.logger.info("Starting game server \"%s\"." % self.name)

        self.process = Popen(command, stdin=PIPE, stdout=PIPE, cwd=self.path,
                             stderr=PIPE, bufsize=1, universal_newlines=True)

        self.watchdog_thread = Thread(target=self._watchdog)
        self.watchdog_thread.start()

        self.stdout_watcher_thread = Thread(target=self._stdout_watcher)
        self.stdout_watcher_thread.start()

        self.stderr_watcher_thread = Thread(target=self._stderr_watcher)
        self.stderr_watcher_thread.start()

    def check_server_is_running(self):
        """Check if server is running if not raise ServerNotRunning."""
        if not self.status:
            raise ServerNotRunning(self)

    def write(self, command, add_newline=True):
        r"""Write to stdin of process.

        -**parameters**, **types**, **return** and **return types**

             :param str command: Command for the game server.
             :param boolean add_newline: When true add \n to the command.
        """
        self.check_server_is_running()

        if add_newline:
            command = "%s\n" % command
        self.process.stdin.write(command)
        self.stdin_deque.append((time(), remove_newline(command)))
        self.process.stdin.flush()  # needed for Python3

    def combine(self):
        """Combine output from stdout, stderr and stdin."""
        out = deque()
        out.extend(self.stdin_deque)
        out.extend(self.stdout_deque)
        out.extend(self.stderr_deque)

        return sorted(out, key=lambda line: line[0])
