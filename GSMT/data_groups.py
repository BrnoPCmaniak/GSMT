"""Module for data classes."""


class Adress(object):
    """Store adress."""

    def __init__(self, adress=None, port=None, username=None, password=None):
        """Init :class Adress:.

        -**parameters**, **types**, **return** and **return types**

            :param str adress: Adress (ip, domain name)
            :param int port: Port
            :param str username: username
            :param str password: Password
        """
        self.adress = adress
        self.port = port
        self.username = username
        self.password = password

    def _check_for_error(self):
        """Check if Adress and port is specified otherwise raise exception."""
        if self.adress is None or self.port is None:
            raise Exception("Adress or port not specified.")

    def as_tupple(self):
        """Return tupple (adress, port)."""
        self._check_for_error()
        return (self.adress, self.port)

    def as_url(self):
        """Return HTTP representation of URL."""
        self._check_for_error()
        if self.username is not None and self.password is not None:
            return "http://%s:%s@%s:%d" % (self.username, self.password,
                                           self.adress, self.port)
        elif self.username is not None:
            return "http://%s@%s:%d" % (self.username, self.adress, self.port)
        else:
            return "http://%s:%d" % (self.adress, self.port)


class SystemUser(object):
    """Store data about user and Group."""

    def __init__(self, user, group):
        """Init SystemUser.

        -**parameters**, **types**, **return** and **return types**

            :param str user: System account under which will GSMT daemon run.
            :param str group: System group under which will GSMT daemon run.
        """
        self.user = user
        self.group = group
