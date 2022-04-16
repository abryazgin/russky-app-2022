FROM python:3

RUN apt-get update
RUN apt-get -y install wget systemctl

RUN wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.44.0/otelcol_0.44.0_linux_amd64.deb
RUN dpkg -i otelcol_0.44.0_linux_amd64.deb

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY configs/opentelemetry_collector.yaml /etc/otelcol/config.yaml
COPY ./Makefile .
COPY ./static static
COPY ./templates templates
COPY ./russky russky

CMD [ "make", "run" ]