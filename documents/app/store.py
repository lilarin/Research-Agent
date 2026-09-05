import asyncio

from app.config import Settings, get_settings
from app.resources import open_store


async def initialize_database(settings: Settings) -> None:
    async with open_store(settings) as store:
        await store.setup()


def main() -> None:
    asyncio.run(initialize_database(get_settings()))


if __name__ == "__main__":
    main()
