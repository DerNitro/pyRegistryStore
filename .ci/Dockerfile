FROM python:${PYTHON_VERSION}-alpine

RUN apk --no-cache add py3-coverage && apk --no-cache add pytest

COPY requirements.txt /requirements.txt

RUN /usr/bin/pip3 install --no-cache-dir --upgrade pip \
    && /usr/bin/pip3 install --no-cache-dir --upgrade -r /requirements.txt \
    && rm -rf /tmp/.cache

RUN mkdir -p /app/

VOLUME [ "/app" ]

WORKDIR /app

ENTRYPOINT [ "coverage" ]
