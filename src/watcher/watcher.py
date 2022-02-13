import asyncio
from datetime import datetime

from loguru import logger

from config import Config, Service
from log_formatter import LogFormatter, Response
from telegram import Bot
from watcher.utils import try_ping


class WatcherTask:
    def __init__(self, service_config: Service, config: Config, bot: Bot):
        self.service_config = service_config
        self.config = config
        self.bot = bot

        """Variables used in run() method."""
        self._fails = 0
        self._last_time_accessed = None

    async def run(self):
        while 1:
            try:
                response = await try_ping(self.service_config.url)

            except:  # NOQA: 722
                response = Response()

            await self.registrate_response(response)

    async def registrate_response(self, response):
        if response.ok:
            self._last_time_accessed = datetime.now()
            self._fails = 0
            log = await LogFormatter.format_log(response, self.service_config)
            logger.info(log)
            if self.config.bot_success_logs:
                await self.bot.send_log(log)

        else:
            self._fails += 1

        if self._fails == self.service_config.panic:
            await self.registrate_fail(response)
            self._fails = 0

        waiting_time = self.service_config.interval - response.time
        await asyncio.sleep(waiting_time if waiting_time > 0 else 0)

    async def registrate_fail(self, response):
        log = await LogFormatter.format_log(response, self.service_config)

        log = (
            log + "\nLast time accessed: " + self._last_time_accessed.strftime(self.config.datetime_fmt)
            if self._last_time_accessed
            else log
        )
        logger.error(log)
        await self.bot.send_log(log)

        await asyncio.sleep(self.service_config.after_panic_delay)
