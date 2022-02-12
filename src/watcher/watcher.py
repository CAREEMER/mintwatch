import asyncio

from loguru import logger

from config_loader import Service
from log_formatter import LogFormatter
from telegram import Bot
from watcher.utils import try_ping


async def watcher_task(service_config: Service, bot: Bot):
    fails = 0

    while 1:

        response = await try_ping(service_config.url)
        log = await LogFormatter.format_log(response, service_config)

        if not response.ok:
            fails += 1
        else:
            logger.info(log)
            fails = 0

        if fails == service_config.panic:
            logger.error(log)
            await bot.send_log(log)
            fails = 0

        waiting_time = service_config.interval - response.time
        await asyncio.sleep(waiting_time if waiting_time > 0 else 0)
