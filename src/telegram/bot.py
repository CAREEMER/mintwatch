import aiohttp
import pydantic


class Bot(pydantic.BaseModel):
    token: str
    chat_id: str

    async def send_log(self, text: str):
        telegram_url = f"https://api.telegram.org/bot{self.token}"

        async with aiohttp.ClientSession() as session:
            data = {
                "chat_id": self.chat_id,
                "text": text,
            }
            async with session.post(telegram_url + "/sendMessage", json=data) as response:
                assert response.ok
