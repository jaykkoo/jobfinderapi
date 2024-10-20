#!/usr/bin/env bash

sudo chown -R ubuntu:ubuntu ~/jobfinderapi
virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install -r /home/ubuntu/jobfinderapi/requirements.txt