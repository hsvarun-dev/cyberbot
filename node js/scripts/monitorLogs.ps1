# Ensure "C:\logs" directory exists
$logPath = "C:\logs\SecurityLog.txt"
if (!(Test-Path "C:\logs")) {
    New-Item -ItemType Directory -Path "C:\logs"
}

# Get latest security logs and save to file
Get-WinEvent -LogName Security -MaxEvents 10 | Out-File -FilePath $logPath

# Output success message
Write-Output "Latest security logs saved to $logPath"