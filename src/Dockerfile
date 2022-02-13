FROM python:3.10.0-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
  && apt install -y netcat gettext libgettextpo-dev \
  && pip install --upgrade pip \
  && pip install poetry==1.1.6

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["main.py"]
ENTRYPOINT ["python"]