ARG ENV

################################################################
# Base Image
################################################################
FROM python:3.10.1-slim-bullseye AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /home/ttt

RUN apt-get update && apt-get install -y nodejs npm
# install postcss-cli as a global package (knwon issue)
RUN npm install --global postcss-cli@^8.3.1

################################################################
# Builder Image
################################################################
FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.12

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# install python dependencies
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock README.rst ./
RUN poetry export -f requirements.txt --without-hashes | /venv/bin/pip install -r /dev/stdin

FROM builder AS builder-dev
RUN echo "builder image - layer for development environment"

FROM builder AS builder-prod
RUN echo "builder image - layer for production environment"
COPY . .
RUN poetry build --format wheel && /venv/bin/pip install dist/*.whl
RUN cd src && npm install

FROM builder-${ENV} AS builder
RUN echo "builder image for ${ENV} environment"



################################################################
# Final Image
################################################################
FROM base AS final
COPY --from=builder /venv /venv

FROM final AS final-dev
RUN echo "final image - layer for development environment"

FROM final AS final-prod
RUN echo "final image - layer for production environment"
COPY --from=builder /home/ttt/src/node_modules/ /home/ttt/node_modules/
COPY src ./

FROM final-${ENV} AS final
RUN echo "final image for ${ENV} environment"
ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"

# run Gunicorn WSGI
# config file loaded by Gunicorn: ./gunicorn.conf.py
ENTRYPOINT ["gunicorn"]
