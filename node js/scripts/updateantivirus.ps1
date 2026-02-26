Write-Host "Starting Antivirus Update..."
Start-Process -FilePath "C:\Program Files\Windows Defender\MpCmdRun.exe" -ArgumentList "-SignatureUpdate" -Wait
Write-Host "Antivirus update completed successfully!"