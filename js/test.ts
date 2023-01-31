let chars: string ="中文;；ａ"
console.log(chars.match(/[\u0000-\u00ff]/g))     //半形
console.log(chars.match(/[\u4e00-\u9fa5]/g))     //中文
console.log(chars.match(/[\uff00-\uffff]/g))     //全形