# mintwatch

Easy-to-setup bot, ChatOps project for handling telegram chat logging over docker-compose services, being runned as one of them.

Example usage at /example directory.

## Features:
- ~~Configurable logging~~
- Command handling
- Configurable commands
- Database client to collect services acessibility data

## Running from source:
```shell
cd src
poetry shell
poetry install
python main.py
```

## Running in Docker:
```shell
cd src
vim config.toml
docker build . -t mintwatch
docker run mintwatch
```

## Running in docker-compose:
- See /example directory
- Include bot build in services, be sure to write proper config (e.g. write url as the name of the service in docker-compose)


## Base config params:
`token` - telegram bot token

`chat_id` - id of the chat to populate logs
(bot needs to be in the chat if that is the group or you need tomessage him first if you want it to populate logs in private messages)

`bot_success_logs` - 0 or 1 - determines if success logs being populated in the telegram
(be aware of amount of useless logs in telegram chat)


## Service config params:
`url` - http url to be pinged

`panic` - how many times ping must be failed before panic log to be populated

`interval` - interval between the pings, in seconds

`after_panic_delay` - delay after populating panic log, in seconds

`success_log` - template of the successful ping log, you can read about possible log kwargs in section below

`failure_log` - same thing, but for failed pings


### Possible log kwargs:
`name` - name of the service

`url` - url of the service

`ok` - if response is ok

`status_code` - status code of the get response

`body` - body of the response (usage is not recommended due to lack of readability of the response body)

`time` - time elapsed during the request
