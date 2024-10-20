#!/usr/bin/env bash

sudo apt update

# Install required system packages
# sudo apt install -y libpq-dev python3-dev
virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install -r /home/ubuntu/jobfinderapi/requirements.txt