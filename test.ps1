# PowerShell helper script to run tests

Write-Host "Running Mailer tests with pytest..." -ForegroundColor Green
python -m pytest -v
