FROM python:slim

WORKDIR /home/game

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
# https://github.com/benoitc/gunicorn/pull/2581#issuecomment-994198667
RUN venv/bin/pip install "https://github.com/benoitc/gunicorn/archive/refs/heads/master.zip#egg=gunicorn==20.1.0"

COPY src/app app
COPY src/tic_tac_toe_game tic_tac_toe_game

COPY game.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP game.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
