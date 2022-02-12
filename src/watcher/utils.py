from time import time

import aiohttp
from pydantic import AnyHttpUrl

from log_formatter import Response


def response_builder(f):
    async def wrapper(*args, **kwargs) -> Response:
        ok, status, body, _time = await f(*args, **kwargs)

        return Response(ok=ok, status_code=status, body=body, time=_time)

    return wrapper


def timeit(f):
    async def wrapper(*args, **kwargs):
        time_1 = time()

        ok, status, body = await f(*args, **kwargs)

        return ok, status, body, time() - time_1

    return wrapper


@response_builder
@timeit
async def try_ping(url: AnyHttpUrl) -> Response:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            # TODO: убрать костыль, подумать как парсить этот респонс в pydantic объект внутри данной функции
            return response.ok, response.status, await response.text()  # NOQA
