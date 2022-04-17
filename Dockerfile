FROM python:3

RUN apt-get update
RUN apt-get -y install wget systemctl

WORKDIR /usr/src/app

#RUN wget https://storage.yandexcloud.net/lib.russky-devops.ru/filebeat-8.1.2-amd64.deb
#RUN wget https://storage.yandexcloud.net/lib.russky-devops.ru/heartbeat-8.1.2-amd64.deb
#RUN wget https://storage.yandexcloud.net/lib.russky-devops.ru/metricbeat-8.1.2-amd64.deb
#RUN dpkg -i filebeat-8.1.2-amd64.deb
#RUN dpkg -i heartbeat-8.1.2-amd64.deb
#RUN dpkg -i metricbeat-8.1.2-amd64.deb
#RUN metricbeat modules enable system

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY configs/opentelemetry_collector.yaml /etc/otelcol/config.yaml
COPY ./Makefile .
COPY ./static static
COPY ./templates templates
COPY ./russky russky

CMD [ "make", "run" ]