# Setup for Windows

Write-Host "Setting up Django Photo Viewer..."
Push-Location $PSScriptRoot
py -m pip install django
py -m pip install pillow

# create .env file with Secret Key and credits
if (-not (Test-Path ".\.env")) {
    New-Item -ItemType File -Name ".\.env"
}
$length = 64
$byteArray = New-Object byte[] $length
Add-Type -TypeDefinition @"
using System;
using System.Security.Cryptography;

public class RNGCrypto
{
    public static void Fill(byte[] bytes)
    {
        using (var rng = new RNGCryptoServiceProvider())
        {
            rng.GetBytes(bytes);
        }
    }
}
"@
[RNGCrypto]::Fill($byteArray)
$secret_key = [Convert]::ToBase64String($byteArray)
$secret_key = "SECRET_KEY=$secret_key"
$secret_key | Out-File -FilePath ".\.env" -Encoding utf8
"CREDITS=[]" | Out-File -FilePath ".\.env" -Append -Encoding utf8

Set-Location .\photo_viewer
py manage.py makemigrations photo_viewer
py manage.py migrate

# Prompt to create super user
$res = Read-Host "Would you like to create a super user? (y/n)" | ForEach-Object { $_.ToLower() }
if ($res -eq "y") {
    py manage.py createsuperuser
}

Pop-Location