Write-Host "Scanning for system vulnerabilities..."
$logs = Get-WinEvent -LogName Security -MaxEvents 10 | Format-Table -AutoSize | Out-String
Write-Host "Scan complete! Check logs for security threats."
$logs