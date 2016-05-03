"""XMLRPC server.

:class VerifyingServer: provides XMLRPC server with HTTP authentication.
"""

from base64 import b64decode

from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer


class VerifyingServer(SimpleXMLRPCServer):
    """SimpleXMLRPCServer with HTTP auth."""

    daemon = None

    def __init__(self, daemon, *args, **kwargs):
        """Initialize SimpleXMLRPCServer with VerifyingRequestHandler.

        -**parameters**, **types**, **return** and **return types**

            :param Daemon daemon: GSMT daemon instance
            :param dict *args: *args for SimpleXMLRPCServer
            :param dict **kwargs: **kwargs for SimpleXMLRPCServer
        """
        self.daemon = daemon

        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
            """RequestHandler for authentication.

            We use an inner class so that we can call out to the
            authenticate method.
            from http://acooke.org/cute/BasicHTTPA0.html.
            """

            def parse_request(myself):
                """Override parse_request to cehck for auth."""
                if SimpleXMLRPCRequestHandler.parse_request(myself):
                    # if default handler return True we can proceed to auth
                    if self.authenticate(myself.headers):
                        return True
                    else:
                        myself.send_error(401, 'Authentication failed')
                        # in case the credentials are invalid say so
                return False

        # and intialise the superclass with the above
        SimpleXMLRPCServer.__init__(
            self, requestHandler=VerifyingRequestHandler,
            *args, **kwargs)

    def authenticate(self, headers):
        """Check user credentials."""
        basic, encoded = headers.get('Authorization').split(' ')
        assert basic == 'Basic', 'Only basic authentication supported'
        username, password = b64decode(encoded).decode().split(':')
        self.daemon.logger.debug(
            "CONNECTION_ACCEPTED: User %s with password %s" % (
                username, password))
        # TODO: check if username and password is correct
        return True
