import logging

from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.templating import _TemplateResponse

from russky.app import app
from russky.di import DI
from russky.models import RecommendationResponse

logger = logging.getLogger(__name__)


@app.get('/', response_class=HTMLResponse)
@app.get('/recommend', response_class=HTMLResponse)
async def random(request: Request) -> _TemplateResponse:
    logger.info('get absolutely random recommendation')
    return DI.templates.TemplateResponse(
        'recommendations/index.html',
        {'request': request, 'recommendation': DI.data_sources.get_random_recommendation()},
    )


@app.get('/recommend/{recommendation_type}', response_class=HTMLResponse)
async def random_by_type(request: Request, recommendation_type: str) -> _TemplateResponse:
    logger.info(f'get random recommendation for {recommendation_type}')
    return DI.templates.TemplateResponse(
        'recommendations/index.html',
        {'request': request, 'recommendation': DI.data_sources.get_random_recommendation_by_type(recommendation_type)},
    )


@app.get('/api/random')
async def api_random() -> RecommendationResponse:
    return RecommendationResponse(recommendation=DI.data_sources.get_random_recommendation())


@app.get('/health')
async def health() -> str:
    return 'OK'
