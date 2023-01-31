var chars = "【中文字幕】巨乳女教師的誘惑_蓮實克蕾兒《專營無碼無修.偷拍流出.本土國產》";
console.log(chars.match(/[\u0000-\u00ff]/g)); //半形
console.log(chars.match(/[\u4e00-\u9fa5]/g)); //中文
console.log(chars.match(/[\uff00-\uffff]/g)); //全形
console.log(chars.match(/[\u3000\u3001-\u303F]/g), '中日韓標點符號');
console.log(chars.match(/[\uFF01-\uFF5E]/g), '全形英文及標點符號');
console.log(chars.match(/[\u3000-\u3003\u3008-\u300F\u3010-\u3011\u3014-\u3015\u301C-\u301E]/g),'台灣常用標點符號'); //全形標點符號
chars.match(/[\u3000\u3001-\u303F]/g).forEach(e =>{
  console.log(e, e.charCodeAt(0));
})