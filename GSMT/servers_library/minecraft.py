"""This module contains gameservers for minecraft."""
from GSMT.game_server import Server


class VanilaMinecraftServer(Server):
    """Server class for vanila Minecraft server"""
    def start(self):
        self._start(["java", "-Xms1024M", "-Xmx2048M", "-jar",
                     self.path + "minecraft_server.1.9.2.jar", "nogui"])
