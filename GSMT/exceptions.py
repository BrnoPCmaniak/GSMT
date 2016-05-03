"""Exceptions for GSMT Module."""


class GSMTException(Exception):
    """Base Exception for GSMT module."""

    pass


class ServerNotRunning(GSMTException):
    """Exception for operation which requires running game server."""

    def __init__(self, server):
        """Create message."""
        self.msg = "Server \"%s\"is not running " % server.name
