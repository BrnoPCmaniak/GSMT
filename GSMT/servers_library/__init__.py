"""Library of Game servers."""

from GSMT.servers_library.minecraft import VanilaMinecraftServer

GAME_SERVERS = {
    None: None,
    'minecraft_vanila': VanilaMinecraftServer,
}

__all__ = ['VanilaMinecraftServer']
