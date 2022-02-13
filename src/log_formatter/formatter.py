import re

from config import Service
from log_formatter.response import Response


class LogFormatter:
    response_attr_cache = ()

    @classmethod
    async def format_log(cls, response: Response, service_config: Service) -> str:
        template = service_config.success_log if response.ok else service_config.failure_log
        log = template

        attr_map = await cls.get_attr_map(response, service_config)

        regex = re.compile(r"\{([a-zA-Z_]+)\}")
        results = regex.findall(template)
        for group in results:
            log = log.replace("{" + group + "}", attr_map.get(group))

        return log

    @classmethod
    async def get_attr_map(cls, response: Response, service_config: Service):
        trim_keys = ("body",)
        attr_map = {"url": service_config.url, "name": service_config.name}

        await cls.fill_response_attr_cache(response)

        for attr in cls.response_attr_cache:
            value = str(getattr(response, attr, None))
            if attr in trim_keys:
                value = await cls.trim_attr(value)

            attr_map[attr] = value

        return attr_map

    @classmethod
    async def fill_response_attr_cache(cls, response):
        if not cls.response_attr_cache:
            cls.response_attr_cache = tuple([key for key, _ in response])

    @classmethod
    async def trim_attr(cls, attr):
        max_len_of_the_attr = 51  # Length of the default body of the Response obj (/telegram/response.py)

        trim_chars = ("\n", "\r")
        for char in trim_chars:
            attr = attr.replace(char, "")
        if len(attr) > max_len_of_the_attr:
            attr = f'"{attr[:max_len_of_the_attr]}..."'

        return attr
