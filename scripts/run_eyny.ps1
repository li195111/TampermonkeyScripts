conda activate download
Write-Host "Start download"
python $PSScriptRoot/../eyny_url_download.py
Write-Host "Finish download"
Write-Host "Start Update Database"
python $PSScriptRoot/../av.py
Write-Host "Finish Update Database"
Write-Host "Start Housekeep"
python $PSScriptRoot/../housekeep_video.py
Write-Host "Finish Housekeep"