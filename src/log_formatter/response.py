from pydantic import BaseModel, validator


class Response(BaseModel):
    ok: bool = False
    status_code: int = 666
    body: str = "Inaccessible url, this request raised an exception!"
    time: float = 0.0

    @validator("time")
    def trim_time(cls, v):
        trim_digits_to = 3

        str_v = str(v)

        return float(str_v[: str_v.find(".") + trim_digits_to + 1])
