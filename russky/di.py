from opentelemetry import trace
from starlette.templating import Jinja2Templates

from russky.data_sources import MulitpleDataSources
from russky.settings import DataSourceSetting


class DI:
    data_sources = MulitpleDataSources(DataSourceSetting())
    templates = Jinja2Templates(directory='templates')
    tracer_provider = trace.get_tracer_provider()
