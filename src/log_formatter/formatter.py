import re

from config_loader import Service
from log_formatter.response import Response


class LogFormatter:
    @classmethod
    async def format_log(cls, response: Response, serivce_config: Service) -> str:
        template = serivce_config.success_log if response.ok else serivce_config.failure_log
        log = template

        regex = re.compile(r"\{([a-zA-Z_]+)\}")
        results = regex.findall(template)
        for group in results:
            log = log.replace("{" + group + "}", str(getattr(response, group, None)))

        return log
