# PowerShell helper script for code formatting with black

Write-Host "Formatting Python code with black..." -ForegroundColor Green
python -m black subscribers.py email_sender.py web.py __init__.py

Write-Host "Formatting complete!" -ForegroundColor Green
