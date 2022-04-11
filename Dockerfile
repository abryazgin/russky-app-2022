FROM python:3

ENV OTEL_RESOURCE_ATTRIBUTES='service.name=russky-app-2022,service.version=1.0,deployment.environment=dev'
ENV OTEL_EXPORTER_OTLP_ENDPOINT='http://0.0.0.0:8200'

RUN apt-get update
RUN apt-get -y install wget systemctl
RUN wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.44.0/otelcol_0.44.0_linux_amd64.deb
RUN dpkg -i otelcol_0.44.0_linux_amd64.deb

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY opentelemetry_collector.yaml /etc/otelcol/config.yaml
COPY . .

CMD [ "make", "run" ]