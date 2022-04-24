import logging
import os

import ecs_logging
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


def setup_tracing():
    apm = make_apm_client()
    app.add_middleware(ElasticAPM, client=apm)


def setup_logging():
    handler = logging.FileHandler(os.getenv('LOG_PATH', '/var/log/russky/application.log'))
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
    )


setup_logging()
setup_tracing()

import russky.routes  # noqa # for
