# Setup for Windows

Write-Host "Setting up Django Photo Viewer..."
py -m pip install django
py -m pip install pillow

Set-Location .\photo_viewer
py manage.py makemigrations photo_viewer
py manage.py migrate

# Prompt to create super user
$res = Read-Host "Would you like to create a super user? (y/n)" | ForEach-Object { $_.ToLower() }
if ($res -eq "y") {
    py manage.py createsuperuser
}

