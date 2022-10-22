#!/usr/bin/env sh

gunicorn main:app --bind 0.0.0.0:8000 --reload -w 4