# mintwatch

Easy-to-setup bot, ChatOps project for handling telegram chat logging over docker-compose services, being runned as one of them.

Example usage at /example directory.

## Running from source:
```shell
cd src
poetry shell
poetry install
python main.py
```

## Running in Docker:
TODO

## Running in docker-compose:
See /example directory

## Base config params:
```shell
token - telegram bot token

chat_id - id of the chat to populate logs (bot needs to be in the chat if that is the group or you need to
message him first if you want it to populate logs in private messages)
```

## Service config params:
```shell
url - http url to be pinged

panic - how many times ping must be failed before panic log to be populated

interval - interval between the pings, in seconds

after_panic_delay - delay after populating panic log, in seconds

success_log - template of the successful ping log, you can read about possible log kwargs in section below, leave blank to not
populate success logs

failure_log - same thing, but for failed pings
```

### Possible log kwargs:
```shell
url - url of the service

ok - if response is ok

status_code - status code of the get response

body - body of the response (usage is not recommended due to lack of readability of the response body)

time - time elapsed during the request
```