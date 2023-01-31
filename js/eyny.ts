// ==UserScript==
// @name         EynyVideoDownloader
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  try to take over the world!
// @author       You
// @match        http://video.eyny.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=eyny.com
// @grant        none
// ==/UserScript==

(function () {
  'use strict';

  const bot_name: string = 'eyny_bot_';
  const maxLength: number = 100;
  function download_blob(blob: Blob, account_str: string, file_name: string, type_name: string) {
    var today: Date = new Date();
    var timestamp: string = today.getUTCFullYear().toString() + (today.getUTCMonth() + 1).toString() + today.getUTCDate().toString();

    var file_path: string = bot_name + account_str.substring(0,60) + '_' + timestamp + '_' + type_name + '_' + file_name + '.txt';

    var url: string = URL.createObjectURL(blob);
    console.log('Download:', file_path);
    var link_e: HTMLAnchorElement = document.createElement("a");
    link_e.href = url;
    link_e.download = file_path;
    document.body.appendChild(link_e);
    link_e.click();
    document.body.removeChild(link_e);
  }
  function toCDB(chars: string | null) {
    var tmp = "";
    if (chars != null) {
      for (var i = 0; i < chars.length; i++) {
        if (chars.charCodeAt(i) > 65248 && chars.charCodeAt(i) < 65375) {
          tmp += String.fromCharCode(chars.charCodeAt(i) - 65248);
        }
        else { tmp += String.fromCharCode(chars.charCodeAt(i)); }
      }
    }
    return tmp
  }
  function toUnderLine(chars: string | null) {
    var tmp = '';
    if (chars != null) {
      let full_symbos = chars.match(/[\u3000\u3001-\u303F]/g);
      for (var i = 0; i < chars.length; i++) {
        let c = chars.at(i);
        if (c != null) {
          if (full_symbos != null && full_symbos.includes(c)) {
            tmp += '_';
          }
          else {
            tmp += c;
          }
        }
      }
    }
    tmp = tmp.replace(' ', '_');
    tmp = tmp.replace('.', '_');
    while (tmp.includes('__')) {
      tmp = tmp.replace('__', '_');
    }
    return tmp;
  }
  function filter_name(name: string|null){
    let filter_strs:string[] = ['《歐美日韓.無碼無修.偷拍流出.本土國產》','【自提征用】','《專營無碼無修.偷拍流出.本土國產》','《無修正.偷拍.口交.爆乳.中出.內射.流出.國產.本土.露臉.無碼》','《中文.內射.口交.爆乳.中出.中字.高清.HD.可愛》','《中文.內射.口交.爆乳.中出.中字.高清.HD》'];
    for(let str of filter_strs){
      name = name? name.replace(str,'') : name;
    }
    return name
  }
  function parse_video(e: MouseEvent) {
    console.log('Parse Video');
    const btn: HTMLElement = (e.target as HTMLElement);
    const video_container = btn.parentElement;
    if (video_container != null) {
      var vid_name: string | null = '';
      let ele = document.querySelector('.fixwidth font');

      if (ele != null) {
        vid_name = toCDB(filter_name(ele.childNodes[0].textContent));


        vid_name = toUnderLine(vid_name);
        if (vid_name != null) {
          vid_name = vid_name.trim();
          if (vid_name.length > maxLength) {
            vid_name = vid_name.substring(0, maxLength)
          }
        }
      }
      let video_source: HTMLVideoElement | null = video_container.querySelector('video source');
      if (video_source != null) {
        let blob: Blob | null = null;
        let path_name: string = '';
        let path_split: string[] = [];
        let file_name: string = '';
        let src = video_source.src;

        blob = new Blob([src], { type: "text/plain;charset=utf-8" });
        path_name = new URL(src).pathname;
        path_split = path_name.split('/');
        file_name = path_split[path_split.length - 1];
        download_blob(blob, vid_name, file_name, 'vid');
      }
    }
  }
  function onUrlChange() {
    var curr_url = location.href;
    var url_path = location.pathname;
    var area: Element | null = null;
    var urlChangeIntervalID: NodeJS.Timer | null = null;
    var button = document.createElement("Button");
    button.innerHTML = "Download";
    button.id = 'download';
    if (url_path == '/') {
      console.log('Change to Main Page!');
      // mainPageArticles();
    }
    else if (url_path.match('/channel/*') != undefined) {
      console.log('Video List Page!');
      button.setAttribute('style', 'top:70px;right:20px;width: 120px;height: 30px;position:absolute;z-index: 9999;border: 1px #88EEFF;;border-radius: 8px;text-align: center;')
      button.onclick = () => {
        // parse_stories();
      }
      urlChangeIntervalID = setInterval(() => {
        // var btn: HTMLElement | null = document.querySelector('._aa64 button');
        // if (btn != null) {
        //   btn.click();
        // }
        // area = document.querySelector('div._ac0b');
        // if (area != undefined && area != null) {
        //   area.appendChild(button);
        //   if (urlChangeIntervalID != null) {
        //     clearInterval(urlChangeIntervalID);
        //   }
        // }
      }, 1000);
    }
    else if (url_path.match('/watch*') != undefined) {
      console.log('Video Player Page!');
      button.setAttribute('style', 'top:20px;right:20px;width: 120px;height: 30px;position:absolute;z-index: 9999;border: 1px #88EEFF;;border-radius: 8px;text-align: center;')
      button.onclick = (e) => {
        // parse_post(e);
      }
      urlChangeIntervalID = setInterval(() => {
        // area = document.querySelector('article._aatb ._aatk');
        // if (area != undefined && area != null) {
        //   area.appendChild(button);
        //   if (urlChangeIntervalID != null) {
        //     clearInterval(urlChangeIntervalID);
        //   }
        // }
      }, 1000);
    }
  }
  // let mainPageIntervalID: NodeJS.Timer | null = null;
  var last_url = location.href;
  var observer = new MutationObserver(() => {
    if (location.href !== last_url) {
      last_url = location.href;
      onUrlChange();
    }
  })
  observer.observe(document, { subtree: true, childList: true });
  if (location.pathname == '/') {
    console.log('Main Page!');
    // mainPageIntervalID = setInterval(mainPageArticles, 100);
  } else if (location.pathname.match('/watch*') != undefined) {
    var button = document.createElement("Button");
    button.innerHTML = "Download";
    button.id = 'download';
    button.setAttribute('style', 'top:10px;right:20px;width: 120px;height: 30px;position:absolute;z-index: 9999;border: 1px #88EEFF;;border-radius: 8px;text-align: center;')
    button.onclick = (e) => {
      parse_video(e);
    }
    let load_video_interval = setInterval(() => {
      let video_container: HTMLElement | null = document.querySelector('#video_container');
      if (video_container != null) {
        video_container.appendChild(button);
        if (load_video_interval != null) {
          clearInterval(load_video_interval);
        }
      }
    }, 100);
  }
})();