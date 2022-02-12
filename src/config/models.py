from datetime import datetime
from typing import List, Optional

import pydantic

from telegram import Bot


class Service(pydantic.BaseModel):
    url: pydantic.AnyHttpUrl
    panic: int = 3
    interval: int = 5
    after_panic_delay: int = 10
    after_exception_delay: int = 100

    success_log: str = "Base log template - success {response_code} - {body} - {time}"
    failure_log: str = "Base log template - success {response_code} - {body} - {time}"


class Config(pydantic.BaseModel):
    token: str
    service_configs: List[Service] = []
    bot: Optional[Bot]
    chat_id: str
    datetime_fmt: str = "%H:%M:%S %d-%m-%Y"

    @pydantic.validator("datetime_fmt")
    def validate_fmt(cls, v):
        try:
            datetime.now().strftime(v)
        except:  # NOQA 722
            raise ValueError("Not valid datetime format! Check the config")
