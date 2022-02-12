import aiohttp
import pydantic
import requests
from loguru import logger


class Bot(pydantic.BaseModel):
    token: str
    chat_id: str

    @pydantic.validator("token")
    def existing_bot(cls, v):
        response = requests.get(f"https://api.telegram.org/bot{v}/getMe")
        if not response.status_code == 200:
            raise ValueError("Not working bot token! Check the config!")

        logger.info("Initialized bot {}".format(response.json()["result"]["username"]))
        return v

    async def send_log(self, text: str):
        telegram_url = f"https://api.telegram.org/bot{self.token}"

        async with aiohttp.ClientSession() as session:
            data = {
                "chat_id": self.chat_id,
                "text": text,
            }
            async with session.post(telegram_url + "/sendMessage", json=data) as response:
                assert response.ok
