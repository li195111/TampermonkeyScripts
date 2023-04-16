// ==UserScript==
// @name         InstagramDownloader
// @namespace    http://tampermonkey.net/
// @version      0.5
// @description  try to take over the world!
// @author       You
// @match        https://www.instagram.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=instagram.com
// @grant        none
// ==/UserScript==
(function () {
    'use strict';
    function download_blob(blob, account_str, file_name, type_name) {
        var today = new Date();
        var timestamp = today.getUTCFullYear().toString() + (today.getUTCMonth() + 1).toString() + today.getUTCDate().toString();
        var file_path = 'ig_bot_' + account_str + '_' + timestamp + '_' + type_name + '_' + file_name + '.txt';
        var url = URL.createObjectURL(blob);
        console.log('Download:', file_path);
        var link_e = document.createElement("a");
        link_e.href = url;
        link_e.download = file_path;
        document.body.appendChild(link_e);
        link_e.click();
        document.body.removeChild(link_e);
    }
    function post_next_btn(article) {
        var next_btns = Array.from(article.querySelectorAll('button._afxw'));
        var filted_next_btns = [];
        for (var _i = 0, next_btns_1 = next_btns; _i < next_btns_1.length; _i++) {
            var btn = next_btns_1[_i];
            filted_next_btns.push(btn);
        }
        return filted_next_btns;
    }
    function parse_post(e) {
        console.log('Parse Post');
        var btn = e.target;
        var article = btn.parentElement;
        var loaded_imgs = [];
        var loaded_vids = [];
        var n_loaded_imgs = 0;
        var n_loaded_vids = 0;
        var img_srcs = [];
        var vid_srcs = [];
        var filted_next_btns = [];
        if (article != null) {
            loaded_imgs = Array.from(article.querySelectorAll('._aagv')); // 多張照片
            loaded_vids = Array.from(article.querySelectorAll('.xg10s4p')); // 多張影片
            filted_next_btns = post_next_btn(article);
            n_loaded_imgs = loaded_imgs.length;
            n_loaded_vids = loaded_vids.length;
        }
        if (n_loaded_imgs > 0 || n_loaded_vids > 0) {
            if (n_loaded_imgs > 0) {
                var img = loaded_imgs[0].querySelector('img');
                if (img != null && !img_srcs.includes(img.src)) {
                    img_srcs.push(img.src);
                }
            }
            if (n_loaded_vids > 0) {
                var vid = loaded_vids[0].querySelector('video');
                if (vid != null && !vid_srcs.includes(vid.src)) {
                    vid_srcs.push(vid.src);
                }
            }
        }
        var parseTimes = 0;
        var parseId = setInterval(function () {
            var _a;
            if ((n_loaded_imgs >= 1 || n_loaded_vids >= 1) && filted_next_btns.length > 0 && parseTimes < 10) {
                if (n_loaded_imgs >= 1) {
                    var img = loaded_imgs[n_loaded_imgs - 1].querySelector('img');
                    if (img != null && !img_srcs.includes(img.src)) {
                        img_srcs.push(img.src);
                    }
                }
                if (n_loaded_vids >= 1) {
                    var vid = loaded_vids[n_loaded_vids - 1].querySelector('video');
                    if (vid != null && !vid_srcs.includes(vid.src)) {
                        vid_srcs.push(vid.src);
                    }
                    ;
                }
                filted_next_btns[filted_next_btns.length - 1].click();
                if (article != null) {
                    loaded_imgs = Array.from(article.querySelectorAll('._aagv'));
                    loaded_vids = Array.from(article.querySelectorAll('.xg10s4p'));
                    filted_next_btns = post_next_btn(article);
                    n_loaded_imgs = loaded_imgs.length;
                    n_loaded_vids = loaded_vids.length;
                }
            }
            else {
                var account_e = (_a = article === null || article === void 0 ? void 0 : article.parentElement) === null || _a === void 0 ? void 0 : _a.querySelector('div._aasi div._aaqy a');
                var account_str = '';
                if (account_e != null && account_e.textContent != null) {
                    account_str = account_e.textContent;
                }
                var file_name = window.location.pathname.split('/').filter(function (n) { return n; }).join('_');
                if (file_name == '' && article != null && article.parentElement != null) {
                    var page_links = Array.from(article.parentElement.querySelectorAll('._ab8w ._ae1h ._ae5q a.x1i10hfl'));
                    if (page_links != null) {
                        var page_url = page_links[page_links.length - 1];
                        if (page_url != null) {
                            var page_url_split = page_url.href.split('/').filter(function (n) { return n; });
                            file_name = page_url_split[page_url_split.length - 1];
                        }
                    }
                }
                var blob = null;
                if (img_srcs.length > 0) {
                    blob = new Blob([img_srcs.join('\n')], { type: "text/plain;charset=utf-8" });
                    download_blob(blob, account_str, file_name, 'imgs');
                }
                if (vid_srcs.length > 0) {
                    blob = new Blob([vid_srcs.join('\n')], { type: "text/plain;charset=utf-8" });
                    download_blob(blob, account_str, file_name, 'vids');
                }
                clearInterval(parseId);
            }
        }, 250);
    }
    function parse_stories() {
        console.log('Parse Stories');
        var account_e = document.querySelector('div._ac0b header._ac0k div._ac0o div.x9f619');
        var account_str = '';
        if (account_e != null && account_e.textContent != null) {
            var acct_btn = account_e.querySelector('a');
            if (acct_btn != null && acct_btn.textContent != null) {
                if (location.pathname.match('/stories/highlights/*')) {
                    var acct_url_split = acct_btn.href.split('/').filter(function (e) { return e; });
                    account_str = acct_url_split[acct_url_split.length - 1];
                }
                else {
                    account_str = acct_btn.textContent;
                }
            }
        }
        var curr_story = document.querySelector('div._ac0b');
        if (curr_story != null) {
            var blob = null;
            var path_name = '';
            var path_split = [];
            var file_name = '';
            var img = curr_story.querySelector('img');
            var src;
            if (img != null) {
                src = img.src;
                blob = new Blob([src], { type: "text/plain;charset=utf-8" });
                path_name = new URL(src).pathname;
                path_split = path_name.split('/');
                file_name = path_split[path_split.length - 1];
                download_blob(blob, account_str, file_name, 'img');
            }
            var vid = curr_story.querySelector('video');
            var vid_src = curr_story.querySelector('video source');
            if (vid != null) {
                if (vid_src != null) {
                    src = vid_src.src;
                }
                else {
                    src = vid.src;
                }
                blob = new Blob([src], { type: "text/plain;charset=utf-8" });
                path_name = new URL(src).pathname;
                path_split = path_name.split('/');
                file_name = path_split[path_split.length - 1];
                download_blob(blob, account_str, file_name, 'vid');
            }
        }
    }
    function listArticles(articles) {
        if (articles !== null && articles.length > 0) {
            for (var _i = 0, articles_1 = articles; _i < articles_1.length; _i++) {
                var article = articles_1[_i];
                var area = article.querySelector('._aatk');
                if (area != undefined && area != null) {
                    var area_download_btn = area.querySelector('#download');
                    if (area_download_btn == null) {
                        var button = document.createElement("Button");
                        button.id = 'download';
                        button.innerHTML = "Download";
                        button.style.top = '20px';
                        button.style.right = '20px';
                        button.style.width = '120px';
                        button.style.height = '30px';
                        button.style.position = 'absolute';
                        button.style.zIndex = '9999';
                        button.style.border = 'border: 1px #88EEFF solid';
                        button.style.borderRadius = '8px';
                        button.style.textAlign = 'center';
                        button.onclick = function (e) {
                            parse_post(e);
                        };
                        area.appendChild(button);
                    }
                }
            }
        }
    }
    function mainPageArticles() {
        var articles = Array.from(document.querySelectorAll('article._aatb'));
        var articleDetectorID = setInterval(function () {
            articles = Array.from(document.querySelectorAll('article._aatb'));
            console.log("Detect : ".concat(articles.length, " Articles"));
            listArticles(articles);
        }, 1000);
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
            mainPageArticles();
        }
        else if (url_path.match('/stories/*') != undefined) {
            console.log('Change to Stories Page!');
            button.style.top = '70px';
            button.style.right = '20px';
            button.style.width = '120px';
            button.style.height = '30px';
            button.style.position = 'absolute';
            button.style.zIndex = '9999';
            button.style.border = 'border: 1px #88EEFF solid';
            button.style.borderRadius = '8px';
            button.style.textAlign = 'center';
            button.onclick = function () {
                parse_stories();
            };
            urlChangeIntervalID = setInterval(function () {
                var btn = document.querySelector('._aa64 button');
                if (btn != null) {
                    btn.click();
                }
                area = document.querySelector('div._ac0b');
                if (area != undefined && area != null) {
                    area.appendChild(button);
                    if (urlChangeIntervalID != null) {
                        clearInterval(urlChangeIntervalID);
                    }
                }
            }, 1000);
        }
        else if (url_path.match('/p/*') != undefined) {
            console.log('Change to Post Page!');
            button.style.top = '20px';
            button.style.right = '20px';
            button.style.width = '120px';
            button.style.height = '30px';
            button.style.position = 'absolute';
            button.style.zIndex = '9999';
            button.style.border = 'border: 1px #88EEFF solid';
            button.style.borderRadius = '8px';
            button.style.textAlign = 'center';
            button.onclick = function (e) {
                parse_post(e);
            };
            urlChangeIntervalID = setInterval(function () {
                area = document.querySelector('article._aatb ._aatk');
                if (area != undefined && area != null) {
                    area.appendChild(button);
                    if (urlChangeIntervalID != null) {
                        clearInterval(urlChangeIntervalID);
                    }
                }
            }, 1000);
        }
        else if (url_path.match('/*/')) {
            console.log('Personal Page!');
            // console.log('All Posts');
            // scrollToEnd();
        }
    }
    // var posts: HTMLAnchorElement[];
    // var allPosts: string[] = [];
    // var lastScrollHeight = document.body.scrollHeight;
    // var scrollIntervalID: NodeJS.Timer;
    // var scrollTimeoutCounts = 0;
    // function scrollToEnd() {
    //   scrollIntervalID = setInterval(() => {
    //     // Get All Posts
    //     posts = Array.from(document.querySelectorAll('.x78zum5 div._aa_y article ._aabd a'));
    //     posts.map(p => allPosts.push(p.href));
    //     allPosts = allPosts.filter((v, i, a) => a.indexOf(v) === i);
    //     Scroll Page
    //     window.scrollTo(0, document.body.scrollHeight);
    //     if (lastScrollHeight < document.body.scrollHeight) {
    //       scrollTimeoutCounts = 0;
    //       lastScrollHeight = document.body.scrollHeight;
    //     } else {
    //       scrollTimeoutCounts += 1;
    //       if (scrollTimeoutCounts > 10 * 4) {
    //         clearInterval(scrollIntervalID);
    //       }
    //     }
    //     console.log('Posts:', allPosts.length);
    //   }, 1600);
    // }
    var last_url = location.href;
    var onece = true;
    var observer = new MutationObserver(function () {
        if (location.href !== last_url) {
            last_url = location.href;
            onUrlChange();
        }
        if (onece) {
            onUrlChange();
            onece = false;
        }
    });
    observer.observe(document, { subtree: true, childList: true });
    if (location.pathname == '/') {
        console.log('Main Page!');
        mainPageArticles();
    }
})();
