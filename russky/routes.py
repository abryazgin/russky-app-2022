import logging

from fastapi import Request
from fastapi.responses import HTMLResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.trace import get_tracer
from starlette.templating import _TemplateResponse


from russky.models import RecommendationResponse
from russky.app import app
from russky.di import DI


@app.get('/', response_class=HTMLResponse)
async def read_item(request: Request) -> _TemplateResponse:
    logging.getLogger(__name__).info("get random recommendation log entry")
    with get_tracer(__name__).start_as_current_span("get random recommendation"):
        return DI.templates.TemplateResponse(
            'recommendations/index.html',
            {'request': request, 'recommendation': DI.data_sources.get_random_recommendation()},
        )


@app.get('/api/random')
async def root() -> RecommendationResponse:
    return RecommendationResponse(recommendation=DI.data_sources.get_random_recommendation())


@app.get('/health')
async def health() -> str:
    return 'OK'


FastAPIInstrumentor.instrument_app(app, tracer_provider=DI.tracer_provider)
