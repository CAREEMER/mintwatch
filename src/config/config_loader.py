import toml

from config.models import Config, Service
from telegram import Bot


def load_config():
    toml_obj = toml.load("./config.toml")
    config = Config(**toml_obj.get("BASE"))
    config.bot = Bot(token=config.token, chat_id=config.chat_id)

    for service in config.services:
        config.service_configs.append(Service(**toml_obj.get(service)))

    return config
