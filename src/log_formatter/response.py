from typing import Optional

import pydantic


class Response(pydantic.BaseModel):
    ok: Optional[bool]
    status_code: Optional[int]
    body: Optional[str]
    time: Optional[float]

    async def parse_response(self, response):
        self.ok = response.ok
        self.status_code = response.status_code
        self.body = await response.text("UTF-8")

        return self
