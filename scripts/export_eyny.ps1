$folderPath = (Get-Item $PSScriptRoot).parent
npx tsc $folderPath\js\eyny.ts --lib ES6,DOM