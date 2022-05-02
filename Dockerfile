FROM python:3

RUN apt-get update
RUN apt-get -y install wget systemctl

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /var/log/russky

COPY ./Makefile .
COPY ./static static
COPY ./templates templates
COPY ./russky russky

CMD [ "make", "run" ]