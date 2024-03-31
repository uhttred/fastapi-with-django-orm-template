import logging
import sentry_sdk

from cliver.settings import config


logger = logging.getLogger(__name__)


def init_sentry():
    if config.SENTRY_DSN:
        logger.info('Initializing sentry')
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
            environment=config.ENV_MODE,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
