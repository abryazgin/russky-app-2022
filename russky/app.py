import logging
import os

import ecs_logging
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


def setup_tracing() -> None:
    apm = make_apm_client()
    app.add_middleware(ElasticAPM, client=apm)


def setup_logging() -> None:
    handler = logging.FileHandler(os.getenv('LOG_PATH', 'russky.log'))
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
    )


setup_logging()
setup_tracing()

import russky.routes  # noqa # for
