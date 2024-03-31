import os
import time

from pathlib import Path
from functools import cached_property
from typing import (
    Literal,
    Optional
)

from django.core.asgi import get_asgi_application

from pydantic import AnyUrl
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

from cliver.core.validators.types import (
    ListCommaStringOrAsterisk
)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cliver.settings")

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    # Environment
    SECRET_KEY: str
    DEBUG: bool = False
    TIMEZONE: str = 'UTC'
    ENV_MODE: Literal[
        'test',
        'development',
        'production'
    ] = 'production'

    # CORS
    CORS_ALLOW_ORIGINS: ListCommaStringOrAsterisk[list[AnyUrl]]
    CORS_ALLOW_CREDENTIALS: bool = True

    # Database
    DB_HOST: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_DB: str
    DB_PORT: int = 5432
    DB_SCHEME: str = 'postgresql'

    # Other apps
    SENTRY_DSN: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
        extra='ignore'
    )
    
    @cached_property
    def CORS_ALLOW_ORIGINS_STR(self) -> list[str]:
        return [str(origin).strip('/') for origin in self.CORS_ALLOW_ORIGINS]

    @cached_property
    def DATABASE_URL(self) -> str:
        return '{scheme}://{username}:{password}@{host}/{db}:{port}'.format(
            scheme=self.DB_SCHEME,
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            db=self.DB_DB
        )

    @property
    def in_devmode(self) -> bool:
        return self.ENV_MODE == 'development'
    
    @property
    def in_testmode(self) -> bool:
        return self.ENV_MODE == 'test'

    @property
    def in_prodmode(self) -> bool:
        return self.ENV_MODE == 'production'


config = Settings()  # type: ignore

# Django ORM Support
USE_TZ = True
INSTALLED_APPS = ('cliver',)
SECRET_KEY = config.SECRET_KEY
TIME_ZONE = config.TIMEZONE
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.DB_DB,
        'USER': config.DB_USERNAME,
        'PASSWORD': config.DB_PASSWORD,
        'HOST': config.DB_HOST,
        'PORT': config.DB_PORT,
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': False
    }
}


def set_timezone(timezone: Optional[str] = None) -> None:
    """Configure default timezone"""
    os.environ['TZ'] = timezone or config.TIMEZONE
    time.tzset()


set_timezone()
django_app = get_asgi_application()
