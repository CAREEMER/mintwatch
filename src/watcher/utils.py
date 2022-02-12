from time import time

import aiohttp
from pydantic import AnyHttpUrl

from log_formatter import Response


def timeit(f):
    async def wrapper(*args, **kwargs):
        time_1 = time()

        response = await f(*args, **kwargs)
        response.time = time() - time_1

        return response

    return wrapper


@timeit
async def try_ping(url: AnyHttpUrl) -> Response:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await Response().parse_response(response)

    except:  # NOQA: 722
        return Response()
