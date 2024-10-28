(function () {
  var subject = document.querySelector("#thread_subject").textContent; // 取得標題
  var textContentEle = document.querySelectorAll('.t_f'); // 取得內文
  var textContent = '';
  textContentEle.forEach((e,i) => { 
      if (i <= 14) {
          var split = '\n=============================================================\n';
          textContent += `${split}${e.textContent}`;
          e.querySelectorAll('img').forEach((img) => {
              textContent += `\n${img.src}`;
          });
      }
  });
  var blob = new Blob([textContent], { type: 'text/plain' });
  var downloadUrl = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = downloadUrl;
  a.download = `${subject}.txt`; // 設置下載的文件名
  document.body.appendChild(a); // 將<a>元素添加到文檔中以便能夠觸發點擊事件
  a.click(); // 模擬點擊事件以觸發下載
  document.body.removeChild(a); // 下載後從文檔中移除<a>元素
  URL.revokeObjectURL(downloadUrl); // 釋放由URL.createObjectURL()創建的URL
})(); // temp在這個函數執行完後就不再可訪問
