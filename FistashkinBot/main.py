import disnake
import platform
import random
import datetime
import os

from disnake.ext import tasks
from core import Config, FistashkinBot
from utils import BotActivity, MainSettings
from loguru import logger

if __name__ == "__main__":
    os.system("@cls||clear")
    data_time = datetime.datetime.now().strftime("%d.%m.%Y %H-%M-%S")
    logger.add(sink=f"./logs/{data_time}.log")

    bot = FistashkinBot()
    bot.i18n.load("./localization")
    bot.load_extensions()

    await bot.change_presence(status=disnake.Status.idle)

    @tasks.loop(minutes=60)
    async def change_activity():
        await bot.change_presence(activity=random.choice(BotActivity.ACTIVITY))

    @bot.event
    async def on_ready():
        developer = await bot.fetch_user(MainSettings.DEVELOPER_ID)
        START_MESSAGE = f"""
                     ______   _         _                   _       _      _           ____            _
                    |  ____| (_)       | |                 | |     | |    (_)         |  _ \          | |
                    | |__     _   ___  | |_    __ _   ___  | |__   | | __  _   _ __   | |_) |   ___   | |_
                    |  __|   | | / __| | __|  / _` | / __| | '_ \  | |/ / | | | '_ \  |  _ <   / _ \  | __|
                    | |      | | \__ \ | |_  | (_| | \__ \ | | | | |   <  | | | | | | | |_) | | (_) | | |_
                    |_|      |_| |___/  \__|  \__,_| |___/ |_| |_| |_|\_\ |_| |_| |_| |____/   \___/   \__|
        ----------------------------------------------------------------------------------------------------------------

                                                         Официальный бот!
                                                      ----------------------
                              Discord бот! / Разработчик - {developer.display_name} / Дата создания: {bot.user.created_at.strftime("%d.%m.%Y")}
                                                      ----------------------
                              -----------------------/     {bot.user.display_name}    \----------------------

        ################################################################################################################

        -
        Разработчик - {developer.display_name} (@{developer} ID: {developer.id})
        Бот - {bot.user} (ID: {bot.user.id})
        Пинг бота - {round(bot.latency * 1000)} мс
        Шардов - {bot.shard_count}

        Язык програмирования - Python {platform.python_version()}
        Библиотека разработки - {disnake.__title__} {disnake.__version__}
        -
        """
        change_activity.start()
        vc = disnake.utils.get(
            bot.get_guild(1037792926383747143).channels, id=1191523826585059419
        )
        await vc.guild.change_voice_state(channel=vc, self_mute=False, self_deaf=False)
        logger.info(f"\n - Бот успешно подключен - \n")
        logger.info(START_MESSAGE)

    try:
        bot.run(Config.TOKEN)
    except HTTPException:
        logger.error("Бот временно забанен в Discord из-за наложенного RateLimit!")
        logger.error("Пытаюсь исправить...")
        system("kill 1")
        try:
            bot.run(Config.TOKEN)
        except HTTPException:
            logger.error("Временно запрещен!")
    except Exception as error:
        logger.error(error)
