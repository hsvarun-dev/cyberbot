Write-Output "🔍 Scanning for system vulnerabilities..."

# Check for missing security patches
$missingUpdates = Get-WindowsUpdate -NotInstalled
if ($missingUpdates.Count -gt 0) {
    Write-Output "⚠️ Missing security patches detected!"
    $missingUpdates | Out-File "C:\logs\MissingSecurityUpdates.txt"
} else {
    Write-Output "✅ No missing security patches found!"
}

# Check for misconfigurations
$securityConfig = Get-SecurityPolicySetting
Write-Output "📋 System Security Configuration:"
Write-Output $securityConfig

Write-Output "✅ Vulnerability scan completed!"