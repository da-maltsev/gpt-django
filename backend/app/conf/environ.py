"""Read .env file"""
import environ  # type: ignore

env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

environ.Env.read_env("app/.env")  # reading .env file

__all__ = [
    env,
]
