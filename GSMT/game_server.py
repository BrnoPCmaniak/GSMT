"""Game server classes."""
from collections import deque
from subprocess import PIPE, Popen
from threading import Thread
from time import time

from GSMT.exceptions import ServerNotRunning


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
    watchdog_thread = None

    def __init__(self, name, logger, config, path, buffsize=100):
        """Init game_server."""
        self.name = name
        self.logger = logger
        self.config = config
        self.path = path
        self.stdout_deque = deque(maxlen=buffsize)
        self.stderr_deque = deque(maxlen=buffsize)

        self.logger.debug("Initialized server \"%s\" on path \"%s\"." % (name,
                                                                         path))

    def start(self):
        """Override this method to call self._start."""
        raise NotImplementedError

    def setup(self):
        """Download and setup server."""
        raise NotImplementedError

    def start_on_daemon_start(self):
        """If server option start_on_deamon_start is true start server."""
        if self.config.getboolean("start_on_deamon_start", fallback=False):
            self.start()

    def _stdout_watcher(self):
        """Watch STDOUT output of self.process."""
        start_msg = "Starting STDOUT watcher for %s" % self.name
        self.logger.debug(start_msg)
        self.stdout_deque.append((time(), "GSMT: %s" % start_msg))
        try:
            with self.process.stdout:
                for line in iter(self.process.stdout.readline, ''):
                    self.stdout_deque.append((time(), line))
        finally:
            stop_msg = "Stopping STDOUT watcher for %s" % self.name
            self.logger.debug(stop_msg)
            self.stdout_deque.append((time(), "GSMT: %s" % stop_msg))

    def _stderr_watcher(self):
        """Watch STDERR output of self.process."""
        start_msg = "Starting STDERR watcher for %s" % self.name
        self.logger.debug(start_msg)
        self.stderr_deque.append((time(), "GSMT: %s" % start_msg))
        try:
            with self.process.stderr:
                for line in iter(self.process.stderr.readline, ''):
                    self.stderr_deque.append((time(), line))
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

        self.process = Popen(command, stdin=PIPE, stdout=PIPE,
                             stderr=PIPE, bufsize=1, universal_newlines=True)

        self.watchdog_thread = Thread(targer=self._watchdog, args=[self])
        self.watchdog_thread.start()

        self.stdout_watcher_thread = Thread(target=self._stdout_watcher,
                                            args=[self])
        self.stdout_watcher_thread.start()

        self.stderr_watcher_thread = Thread(target=self._stderr_watcher,
                                            args=[self])
        self.stderr_watcher_thread.start()

    def check_server_is_running(self):
        """Check if server is running if not raise ServerNotRunning."""
        if not self.status:
            raise ServerNotRunning(self)

    def write(self, command, add_newline=True):
        """Write to stdin."""
        self.check_server_is_running()

        if add_newline:
            self.process.stdin.write("%s\n" % command)
        else:
            self.process.stdin.write(command)
        self.process.stdin.flush()  # needed for Python3
