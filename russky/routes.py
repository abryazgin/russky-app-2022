import logging
import uuid

from fastapi import Request
from fastapi.responses import HTMLResponse
from multiavatar.multiavatar import multiavatar
from starlette.responses import Response
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


@app.get('/avatar')
def avatar() -> Response:
    image: bytes = multiavatar(uuid.uuid4().hex, True, None).encode()
    # media_type here sets the media type of the actual response sent to the client.
    return Response(content=image, media_type='image/svg+xml')


@app.get('/health')
async def health() -> str:
    return 'OK'
