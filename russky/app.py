from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from russky.data_sources import MulitpleDataSources
from russky.models import RecommendationResponse
from russky.settings import DataSourceSetting, LoggingSetting

app = FastAPI()
LoggingSetting().setup()
data_sources = MulitpleDataSources(DataSourceSetting())
templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def read_item(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(
        'recommendations/index.html',
        {'request': request, 'recommendation': data_sources.get_random_recommendation()},
    )


@app.get('/api/random')
async def root() -> RecommendationResponse:
    return RecommendationResponse(recommendation=data_sources.get_random_recommendation())


@app.get('/ping')
async def ping() -> str:
    return 'pong'
