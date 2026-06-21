@echo off
REM Helper script for code formatting with black

echo Formatting Python code with black...
python -m black subscribers.py email_sender.py web.py __init__.py

echo Formatting complete!
pause
