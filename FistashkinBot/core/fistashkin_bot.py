import os
import traceback
import disnake

from disnake.ext import commands
from jishaku.modules import find_extensions_in


class FistashkinBot(commands.AutoShardedInteractionBot):
    def __init__(self, *args):
        super().__init__(
            intents=disnake.Intents.all(),
            sync_commands_debug=False,
            chunk_guilds_at_startup=False,
            reload=True,
            # test_guilds=[1156719063087726613],
            *args,
        )

    def load_extensions(self):
        """for filename in os.listdir("./fistashkinbot"):
        if filename.endswith(".py"):
            try:
                self.load_extension(f"fistashkinbot.{filename[:-3]}")
            except Exception as e:
                traceback.format_exc(e)"""

        for folder in os.listdir("fistashkinbot"):
            for cog in find_extensions_in(f"fistashkinbot/{folder}"):
                try:
                    self.load_extension(cog)
                    print(f"[LOAD] {cog} loaded!")
                except Exception as e:
                    print(f"[ERROR] {folder}.{cog} fucked up by Hueila: {e}")
