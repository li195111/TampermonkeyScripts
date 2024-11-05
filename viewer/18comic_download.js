let dropdownMenuList = document.querySelectorAll('.dropdown-menu'); // get all dropdown menu

// dropdownMenuList[dropdownMenuList.length -1] // Get the last dropdown menu (Comic List)
Array.from(dropdownMenuList[dropdownMenuList.length -1].querySelectorAll('li a')).map(e => e.href) // Get all download links

document.querySelector('#timer').innerHTML = 0 // skip timer

document.querySelector('#captcha_image') // captcha image

document.querySelector('#invite_verification') // Validation Code Input

document.querySelector('#download_submit') // Download Button