from datetime import datetime
from typing import List, Optional

import requests
from pydantic import AnyHttpUrl, BaseModel, PositiveInt, validator

from telegram import Bot


class Service(BaseModel):
    name: str
    url: AnyHttpUrl
    panic: PositiveInt = 3
    interval: PositiveInt = 5
    after_panic_delay: PositiveInt = 10

    success_log: str = "{name} - SUCCESS\n{url} - {status_code} - {body} - {time}s"
    failure_log: str = "{name} - FAILURE\n{url} - {status_code} - {body} - {time}s"

    @validator("url")
    def is_accessible_url(cls, v):
        try:
            requests.get(v)
        except Exception as e:
            raise ValueError(
                "An exception occured while trying to reach {}:\n{}\n{}\n"
                "Probably because of that this url ({}) is inaccessible. Check the config!".format(v, type(e), e, v)
            )
        return v


class Config(BaseModel):
    token: str
    service_configs: List[Service] = []
    bot: Optional[Bot]
    chat_id: str
    datetime_fmt: str = "%H:%M:%S %d-%m-%Y"
    bot_success_logs: bool = False

    @validator("datetime_fmt")
    def validate_fmt(cls, v):
        try:
            datetime.now().strftime(v)
        except:  # NOQA 722
            raise ValueError("Not valid datetime format! Check the config")
