from tortoise import Tortoise

from app.config import Settings, get_settings


def get_tortoise_config(settings: Settings) -> dict[str, object]:
    return {
        "connections": {
            "default": (
                f"postgres://{settings.postgres_user}:{settings.postgres_password}"
                f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
            ),
        },
        "apps": {
            "models": {
                "models": ["src.models.models", "aerich.models"],
                "default_connection": "default",
            },
        },
    }


async def init_database(settings: Settings) -> None:
    await Tortoise.init(config=get_tortoise_config(settings))


async def close_database() -> None:
    await Tortoise.close_connections()


TORTOISE_ORM = get_tortoise_config(get_settings())
