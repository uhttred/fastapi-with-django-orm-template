from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from asgi_correlation_id import CorrelationIdMiddleware

from cliver.settings import config
from cliver.api import router

from cliver.core.sentry import init_sentry
from cliver.core.logger import configure_logger
from cliver.core.middleware import (
    ProcessTimeHeaderMiddleware
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logger()
    yield


init_sentry()

app = FastAPI(
    lifespan=lifespan,
    debug=config.DEBUG,
    redirect_slashes=False,
    version='0.1.0',
    docs_url='/docs' if config.in_devmode else None,
    redoc_url='/redoc' if config.in_devmode else None
)

app.add_middleware(ProcessTimeHeaderMiddleware)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ALLOW_ORIGINS_STR,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        'X-Process-Time'
    ]
)


app.include_router(router)


@app.get('/')
async def welcome():
    return f'Welcome to Cliver, A FastAPI with Django ORM Template!'
