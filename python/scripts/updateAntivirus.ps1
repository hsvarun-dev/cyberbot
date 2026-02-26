$version = (Get-MpComputerStatus).AntivirusSignatureVersion
Write-Output "✅ Antivirus updated! Installed Version: $version"