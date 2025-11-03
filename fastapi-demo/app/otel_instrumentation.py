from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import os

def setup_tracing(service_name: str):
    """Configures OpenTelemetry tracing"""
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318")

    provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: service_name})
    )
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces"))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Instrument key components
    FastAPIInstrumentor().instrument()
    RequestsInstrumentor().instrument()