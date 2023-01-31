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
    var bot_name = 'eyny_bot_';
    var maxLength = 100;
    function download_blob(blob, account_str, file_name, type_name) {
        var today = new Date();
        var timestamp = today.getUTCFullYear().toString() + (today.getUTCMonth() + 1).toString() + today.getUTCDate().toString();
        var file_path = bot_name + account_str.substring(0, 60) + '_' + timestamp + '_' + type_name + '_' + file_name + '.txt';
        var url = URL.createObjectURL(blob);
        console.log('Download:', file_path);
        var link_e = document.createElement("a");
        link_e.href = url;
        link_e.download = file_path;
        document.body.appendChild(link_e);
        link_e.click();
        document.body.removeChild(link_e);
    }
    function toCDB(chars) {
        var tmp = "";
        if (chars != null) {
            for (var i = 0; i < chars.length; i++) {
                if (chars.charCodeAt(i) > 65248 && chars.charCodeAt(i) < 65375) {
                    tmp += String.fromCharCode(chars.charCodeAt(i) - 65248);
                }
                else {
                    tmp += String.fromCharCode(chars.charCodeAt(i));
                }
            }
        }
        return tmp;
    }
    function toUnderLine(chars) {
        var tmp = '';
        if (chars != null) {
            var full_symbos = chars.match(/[\u3000\u3001-\u303F]/g);
            for (var i = 0; i < chars.length; i++) {
                var c = chars.at(i);
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
    function filter_name(name) {
        var filter_strs = ['《歐美日韓.無碼無修.偷拍流出.本土國產》', '【自提征用】', '《專營無碼無修.偷拍流出.本土國產》', '《無修正.偷拍.口交.爆乳.中出.內射.流出.國產.本土.露臉.無碼》', '《中文.內射.口交.爆乳.中出.中字.高清.HD.可愛》', '《中文.內射.口交.爆乳.中出.中字.高清.HD》'];
        for (var _i = 0, filter_strs_1 = filter_strs; _i < filter_strs_1.length; _i++) {
            var str = filter_strs_1[_i];
            name = name ? name.replace(str, '') : name;
        }
        return name;
    }
    function parse_video(e) {
        console.log('Parse Video');
        var btn = e.target;
        var video_container = btn.parentElement;
        if (video_container != null) {
            var vid_name = '';
            var ele = document.querySelector('.fixwidth font');
            if (ele != null) {
                vid_name = toCDB(filter_name(ele.childNodes[0].textContent));
                vid_name = toUnderLine(vid_name);
                if (vid_name != null) {
                    vid_name = vid_name.trim();
                    if (vid_name.length > maxLength) {
                        vid_name = vid_name.substring(0, maxLength);
                    }
                }
            }
            var video_source = video_container.querySelector('video source');
            if (video_source != null) {
                var blob = null;
                var path_name = '';
                var path_split = [];
                var file_name = '';
                var src = video_source.src;
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
        var area = null;
        var urlChangeIntervalID = null;
        var button = document.createElement("Button");
        button.innerHTML = "Download";
        button.id = 'download';
        if (url_path == '/') {
            console.log('Change to Main Page!');
            // mainPageArticles();
        }
        else if (url_path.match('/channel/*') != undefined) {
            console.log('Video List Page!');
            button.setAttribute('style', 'top:70px;right:20px;width: 120px;height: 30px;position:absolute;z-index: 9999;border: 1px #88EEFF;;border-radius: 8px;text-align: center;');
            button.onclick = function () {
                // parse_stories();
            };
            urlChangeIntervalID = setInterval(function () {
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
            button.setAttribute('style', 'top:20px;right:20px;width: 120px;height: 30px;position:absolute;z-index: 9999;border: 1px #88EEFF;;border-radius: 8px;text-align: center;');
            button.onclick = function (e) {
                // parse_post(e);
            };
            urlChangeIntervalID = setInterval(function () {
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
    var observer = new MutationObserver(function () {
        if (location.href !== last_url) {
            last_url = location.href;
            onUrlChange();
        }
    });
    observer.observe(document, { subtree: true, childList: true });
    if (location.pathname == '/') {
        console.log('Main Page!');
        // mainPageIntervalID = setInterval(mainPageArticles, 100);
    }
    else if (location.pathname.match('/watch*') != undefined) {
        var button = document.createElement("Button");
        button.innerHTML = "Download";
        button.id = 'download';
        button.setAttribute('style', 'top:10px;right:20px;width: 120px;height: 30px;position:absolute;z-index: 9999;border: 1px #88EEFF;;border-radius: 8px;text-align: center;');
        button.onclick = function (e) {
            parse_video(e);
        };
        var load_video_interval_1 = setInterval(function () {
            var video_container = document.querySelector('#video_container');
            if (video_container != null) {
                video_container.appendChild(button);
                if (load_video_interval_1 != null) {
                    clearInterval(load_video_interval_1);
                }
            }
        }, 100);
    }
})();
