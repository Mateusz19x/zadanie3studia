@echo off
REM Helper script for linting with pylint

echo Running pylint on Python files...
python -m pylint subscribers.py email_sender.py web.py

pause
