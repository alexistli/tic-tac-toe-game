###########
# BUILDER #
###########

# pull official base image
FROM python:3.10.1-slim-bullseye as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# https://github.com/benoitc/gunicorn/pull/2581#issuecomment-994198667
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels "https://github.com/benoitc/gunicorn/archive/refs/heads/master.zip#egg=gunicorn==20.1.0"


#########
# FINAL #
#########

# pull official base image
FROM python:3.10.1-slim-bullseye

# create directory for the app user
ENV HOME=/home/ttt/
RUN mkdir -p $HOME
WORKDIR $HOME

# create the app user
RUN addgroup --system appuser && adduser --system --group appuser

# create the appropriate directories
# ENV APP_HOME=/home/ttt/app/
# ENV ENGINE_HOME=/home/ttt/tic_tac_toe_game/
# RUN mkdir $APP_HOME
# RUN mkdir $ENGINE_HOME

# install dependencies
RUN apt-get update
RUN apt-get install -y nodejs
RUN apt-get install -y npm

COPY src/tailwind.config.js src/postcss.config.js src/package.json src/package-lock.json $HOME
RUN npm install --global postcss-cli@8.3.1
# RUN npm install

# COPY src/package.json src/package-lock.json $HOME
# RUN npm install --global postcss@8.2.8 postcss-cli@8.3.1
# RUN npm install --global @fullhuman/postcss-purgecss@4.0.2
# RUN npm install --global autoprefixer@10.2.5 tailwindcss@2.0.3

# install dependencies
RUN apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy app and engine
# COPY src/app $APP_HOME
# COPY src/app/static/dist/main.css src/app/static/dist/main.js $APP_HOME/static/

# COPY src/tic_tac_toe_game $ENGINE_HOME

# copy Docker and Flask files
# COPY game.py config.py .env.dev docker-compose.yml docker-compose.override.yml gunicorn.conf.py logging_setup.py $HOME


# chown all the files to the app user
RUN chown -R appuser:appuser $HOME

# change to the app user
USER appuser


# run Gunicorn WSGI
# config file loaded by Gunicorn: ./gunicorn.conf.py
ENTRYPOINT ["gunicorn"]
CMD ["--log-level=debug"]
