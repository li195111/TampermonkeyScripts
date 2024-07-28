$folderPath = (Get-Item $PSScriptRoot).parent
npx tsc $folderPath\js\instagram.ts --lib ES6,DOM