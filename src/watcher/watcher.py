import asyncio
from datetime import datetime

from loguru import logger

from config.config_loader import Config, Service
from log_formatter import LogFormatter
from telegram import Bot
from watcher.utils import try_ping


async def watcher_task(service_config: Service, config: Config, bot: Bot):
    fails = 0
    last_time_accessed = None

    while 1:
        try:
            response = await try_ping(service_config.url)
        except Exception as e:
            await bot.send_log("Can't reach this url - {} Check the config!".format(service_config.url))
            logger.error(
                "An exception occured while trying to reach {}:\n{}\n{}".format(service_config.url, type(e), e)
            )

            await asyncio.sleep(service_config.after_exception_delay)
            continue
        log = await LogFormatter.format_log(response, service_config)

        if response.ok:
            last_time_accessed = datetime.now()
            fails = 0
        else:
            fails += 1

        if fails == service_config.panic:
            log = (
                log + "\nLast time accessed: " + last_time_accessed.strftime(config.datetime_fmt)
                if last_time_accessed
                else log
            )
            logger.error(log)
            await bot.send_log(log)
            fails = 0
            await asyncio.sleep(service_config.after_panic_delay)

        waiting_time = service_config.interval - response.time
        await asyncio.sleep(waiting_time if waiting_time > 0 else 0)
