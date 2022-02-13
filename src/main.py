import asyncio

from config.config_loader import Config, load_config
from watcher import WatcherTask


async def run_tasks(config: Config):
    tasks = []

    for service_config in config.service_configs:
        task = WatcherTask(service_config, config, config.bot)
        tasks.append(task.run())

    await asyncio.gather(*tasks)


def main():
    config = load_config()

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_tasks(config))


if __name__ == "__main__":
    main()
