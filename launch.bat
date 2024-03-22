@echo off
rem Script to launch the server as well as the value updater

call .venv\Scripts\activate

set FLASK_APP=app
start "Flask Server" flask run

python update_pf_value.py