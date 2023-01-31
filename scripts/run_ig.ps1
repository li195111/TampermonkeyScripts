$conda='C:\Users\a0983\miniconda3\shell\condabin\conda-hook.ps1'
wt powershell -noexit -command "& {& $conda\;conda activate scraper\;python $PSScriptRoot\..\ig_url_download.py}"
