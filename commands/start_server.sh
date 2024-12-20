#!/bin/sh

python ./src uvicorn run main:app --reload --host 0.0.0.0 --port 8000
