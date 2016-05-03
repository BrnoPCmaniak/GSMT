"""This module contains gameservers for minecraft."""
import os

from GSMT.game_server import Server


class VanilaMinecraftServer(Server):
    """Server class for vanila Minecraft server.

    - example config file ::

        [main]
        # server with name "main"
        type = minecraft_vanila
        # in direcory /opt/mc_server
        path = /opt/mc_server
        # start server on daemon start
        start_on_daemon_start = True
        # with java <options>
        java_options = -Xms1024M -Xmx2048M
        # name of Jar file
        jar_file = minecraft_server.1.9.2.jar

    """

    def start(self):
        """Start java minecraft server."""
        command = ["java"]

        # Add java options
        command.extend(self._get_java_options())

        # jar file
        command.extend(["-jar", os.path.join(self.path, self._get_jar_file()),
                        "nogui"])
        self._start(command)

    def stop(self):
        """Send stop command to server."""
        self.write("stop")

    def _get_jar_file(self):
        """Return the name of jar_file.

        Default: 'minecraft_server.jar'

        :rtype: str
        """
        return self.config.get("jar_file", "minecraft_server.jar")

    def _get_java_options(self):
        """Return java_options.

        Default: '-Xms1024M -Xmx2048M'

        :rtype: list
        """
        return (self.config.get("java_options", "-Xms1024M -Xmx2048M")
                    .split(" "))
