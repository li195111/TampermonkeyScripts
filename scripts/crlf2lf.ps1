# Define the folder path where you want to search for files
$folderPath = (Get-Item $PSScriptRoot).parent
Write-Host "Searching for files in $folderPath"
# Recursively search for files with the specified extensions
$files = Get-ChildItem -Path $folderPath -File -Recurse

# Loop through each file and replace CRLF with LF
foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $content = $content -replace "`r`n", "`n"
    Set-Content -Path $file.FullName -Value $content
    Write-Host "Replaced CRLF with LF in $($file.FullName)"
}
