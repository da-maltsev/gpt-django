ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim-bullseye as base

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV DATABASE_URL ${DATABASE_URL}
ARG SECRET_KEY

ENV STATIC_ROOT /static

ENV _UWSGI_VERSION 2.0.21

RUN echo deb http://deb.debian.org/debian bullseye contrib non-free > /etc/apt/sources.list.d/debian-contrib.list \
  && apt update \
  && apt --no-install-recommends install -y gettext locales-all wget \
  imagemagick tzdata wait-for-it build-essential \
  && rm -rf /var/lib/apt/lists/*

RUN wget -O uwsgi-${_UWSGI_VERSION}.tar.gz https://github.com/unbit/uwsgi/archive/${_UWSGI_VERSION}.tar.gz \
    && tar zxvf uwsgi-*.tar.gz \
    && UWSGI_BIN_NAME=/usr/local/bin/uwsgi make -C uwsgi-${_UWSGI_VERSION} \
    && rm -Rf uwsgi-*

RUN pip install --upgrade pip

ADD requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /backend
ADD backend /backend

RUN ./manage.py compilemessages
RUN ./manage.py collectstatic --noinput

ARG RELEASE=dev-untagged
#ENV SENTRY_RELEASE ${RELEASE}

USER nobody

CMD sh -c "./manage.py migrate && uwsgi --master --http 0.0.0.0:8000 --module app.wsgi --workers 2 --threads 2 --harakiri 25 --max-requests 500 --log-x-forwarded-for --buffer-size 32000"