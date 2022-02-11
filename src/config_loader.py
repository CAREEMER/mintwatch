from typing import List, Optional

import pydantic
import toml

from telegram import Bot


class Service(pydantic.BaseModel):
    url: pydantic.AnyHttpUrl
    panic: int
    interval: int


class Config(pydantic.BaseModel):
    services: List[str]
    token: str
    service_configs: List[Service] = []
    bot: Optional[Bot]
    chat_id: str


def load_config():
    toml_obj = toml.load("./config.toml")
    config = Config(**toml_obj.get("BASE"))
    config.bot = Bot(token=config.token, chat_id=config.chat_id)

    for service in config.services:
        config.service_configs.append(Service(**toml_obj.get(service)))

    return config
