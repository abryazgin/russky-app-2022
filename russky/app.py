from typing import Dict

from fastapi import FastAPI

from russky.settings import LoggingSetting

app = FastAPI()
LoggingSetting().setup()


@app.get('/')
async def root() -> Dict[str, str]:
    return {'message': 'Hello World'}


@app.get('/ping')
async def ping() -> str:
    return 'pong'
