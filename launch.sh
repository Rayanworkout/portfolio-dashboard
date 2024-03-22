#!/bin/bash

# Script to launch the server as well as the value updater

# Activate the venv

source .venv/bin/activate

flask --app app run

python3 update_pf_value.py