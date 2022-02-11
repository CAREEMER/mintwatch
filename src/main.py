import asyncio

from config_loader import Config, load_config
from watcher import watcher_task


async def run_tasks(config: Config):
    tasks = []

    for service_config in config.service_configs:
        tasks.append(watcher_task(service_config, config.bot))

    await asyncio.gather(*tasks)


def main():
    config = load_config()

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run_tasks(config))


if __name__ == "__main__":
    main()
