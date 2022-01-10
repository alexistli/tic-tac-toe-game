#!/bin/bash
source venv/bin/activate
exec gunicorn -b :5000 --worker-class eventlet -w 1 --log-level=debug game:app
