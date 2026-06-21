# PowerShell helper script for linting with pylint

Write-Host "Running pylint on Python files..." -ForegroundColor Green
python -m pylint subscribers.py email_sender.py web.py
