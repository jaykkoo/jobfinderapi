#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install libpq-dev
virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install -r /home/ubuntu/jobfinderapi/requirements.txt