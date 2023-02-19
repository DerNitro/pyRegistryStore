ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-alpine

RUN apk --no-cache add py3-coverage pytest py3-pip yaml-dev gcc python3-dev linux-headers libc-dev py3-yaml

COPY requirements.txt /requirements.txt

RUN /usr/bin/pip3 install --no-cache-dir --upgrade pip \
    && /usr/bin/pip3 install --no-cache-dir --upgrade -r /requirements.txt \
    && rm -rf /tmp/.cache

RUN mkdir -p /app/

VOLUME [ "/apps" ]

WORKDIR /apps

ENTRYPOINT [ "coverage" ]
