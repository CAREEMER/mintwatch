import pydantic


class Response(pydantic.BaseModel):
    ok: bool
    status_code: int
    body: str
    time: float

    @pydantic.validator("time")
    def trim_time(cls, v):
        trim_digits_to = 3

        str_v = str(v)

        return float(str_v[: str_v.find(".") + trim_digits_to + 1])
