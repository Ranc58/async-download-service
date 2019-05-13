FROM python:3.7-alpine3.7

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_SHELL_COMPAT=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true


RUN apk update \
    && apk upgrade && apk add bash zip && rm -vrf /var/cache/apk/*


RUN mkdir /app
COPY app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app
