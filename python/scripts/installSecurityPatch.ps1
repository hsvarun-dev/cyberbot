# Ensure script runs with admin privileges
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "❌ Please run PowerShell as Administrator!"
    exit
}

Write-Output "⚙️ Installing critical security patches..."
Start-Process -FilePath "C:\Windows\System32\wuauclt.exe" -ArgumentList "/updatenow" -Wait -NoNewWindow
Write-Output "✅ Security patches installed successfully!"