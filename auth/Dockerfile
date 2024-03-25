FROM python:3.10-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential libmariadb-dev libmariadb3 curl \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /tmp/mdbccbin
RUN curl -O https://downloads.mariadb.com/Connectors/c/connector-c-3.3.1/mariadb-connector-c-3.3.1-ubuntu-bionic-amd64.tar.gz \
 && tar xvf mariadb-connector-c-3.3.1-ubuntu-bionic-amd64.tar.gz --directory /usr --strip-components 1 \
 && echo "/usr/lib/mariadb/" > /etc/ld.so.conf.d/mariadb.conf \
 && ldconfig

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 4000

CMD ["python3", "main.py"]
