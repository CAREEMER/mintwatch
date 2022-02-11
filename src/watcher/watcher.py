import asyncio

from loguru import logger

from config_loader import Service
from telegram import Bot
from watcher.utils import try_ping


async def watcher_task(service_config: Service, bot: Bot):
    fails = 0

    while 1:

        response_ok, status_code, time = await try_ping(service_config.url)

        if not response_ok:
            fails += 1
        else:
            logger.info("[{}] SUCCESS: {}, TIME - {}".format(status_code, service_config.url, time))
            fails = 0

        if fails == service_config.panic:
            log = "[{}] ONE WATCH FAILED: {}, TIME - {}".format(status_code, service_config.url, time)
            logger.error(log)
            await bot.send_log(log)
            fails = 0

        await asyncio.sleep(service_config.interval - time)
