#!/usr/bin/env bash

sudo chown -R ubuntu:ubuntu ~/jobfinderapi
virtualenv /home/ubuntu/jobfinderapi/venv
source /home/ubuntu/jobfinderapi/venv/bin/activate
pip install -r /home/ubuntu/jobfinderapi/requirements.txt