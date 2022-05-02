import logging
import os

import ecs_logging
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


def setup_tracing() -> None:
    if not os.getenv('ELASTIC_APM_SERVICE_NAME'):
        return

    apm = make_apm_client()
    app.add_middleware(ElasticAPM, client=apm)


def setup_logging() -> None:
    file_handler = logging.FileHandler(os.getenv('LOG_PATH', 'russky.log'))
    file_handler.setFormatter(ecs_logging.StdlibFormatter())
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            os.getenv(
                'LOF_FORMAT',
                '%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s',
            )
        )
    )
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
    )


setup_logging()
setup_tracing()

import russky.routes  # noqa # for
