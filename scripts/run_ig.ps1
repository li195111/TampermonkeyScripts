conda activate download
Write-Host "Start download"
python $PSScriptRoot/../ig_url_download.py
Write-Host "Finish download"
Write-Host "Start Update Database"
python $PSScriptRoot/../ig.py
Write-Host "Finish Update Database"
