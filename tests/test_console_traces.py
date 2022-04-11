# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, ConcurrentMultiSpanProcessor
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

multiSpanProcessor = ConcurrentMultiSpanProcessor()
multiSpanProcessor.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(TracerProvider(active_span_processor=multiSpanProcessor))
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("foo"):
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello world from OpenTelemetry Python!")
