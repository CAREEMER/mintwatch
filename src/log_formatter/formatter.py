import re

from config import Service
from log_formatter.response import Response


class LogFormatter:
    @classmethod
    async def format_log(cls, response: Response, serivce_config: Service) -> str:
        trim_attrs = ("body",)

        template = serivce_config.success_log if response.ok else serivce_config.failure_log
        log = template

        log = log.replace("{url}", serivce_config.url)

        regex = re.compile(r"\{([a-zA-Z_]+)\}")
        results = regex.findall(template)
        for group in results:
            replace_to = (
                str(getattr(response, group, None))[:30] if group in trim_attrs else str(getattr(response, group, None))
            )
            log = log.replace("{" + group + "}", replace_to)

        return log
