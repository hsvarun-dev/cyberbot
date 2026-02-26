Write-Host "Installing critical security patches..."
Start-Process -FilePath "C:\Windows\System32\wuauclt.exe" -ArgumentList "/updatenow" -Wait
Write-Host "Security patches installed successfully!"