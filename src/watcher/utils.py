from time import time

import aiohttp
from pydantic import AnyHttpUrl
from typing import Tuple


def timeit(f):
    async def wrapper(*args, **kwargs):
        time_1 = time()

        result = await f(*args, **kwargs)

        return *result, time() - time_1

    return wrapper


@timeit
async def try_ping(url: AnyHttpUrl) -> Tuple[bool, int]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response.ok, response.status

    except:
        return False, 0
