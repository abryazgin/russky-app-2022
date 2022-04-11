import logging

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc._metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer
from starlette.templating import _TemplateResponse

from russky.data_sources import MulitpleDataSources
from russky.models import RecommendationResponse
from russky.settings import DataSourceSetting, LoggingSetting

app = FastAPI()
LoggingSetting().setup()
data_sources = MulitpleDataSources(DataSourceSetting())
templates = Jinja2Templates(directory='templates')

tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
OTLPMetricExporter
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def read_item(request: Request) -> _TemplateResponse:
    logging.getLogger(__name__).info("get random recommendation log entry")
    with get_tracer(__name__).start_as_current_span("get random recommendation") :
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


FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
