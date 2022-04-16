from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from russky.settings import LoggingSetting

LoggingSetting().setup()

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

import russky.routes  # noqa # for


def install_opentelemetry():
    tracer_provider = TracerProvider()
    trace.set_tracer_provider(tracer_provider)
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)


install_opentelemetry()
