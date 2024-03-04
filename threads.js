(function(){
    var user = document.URL.split('@')[1]; // 使用者名稱
    var posts = document.querySelectorAll('div.xrvj5dj.xd0jker.x1wxlsmb'); // Threads貼文
    posts.forEach((post) => {
        if(post.querySelector('div.xpvyfi4.x1xdureb.x1agbcgv a').textContent == user){
            console.log(post); // 貼文者
            var textContent = post.querySelector('div.x1xdureb.xqti54a.x13vxnyz div.x1a6qonq.x6ikm8r.x10wlt62.xj0a0fe.x126k92a.x6prxxf.x7r5mf7'); // 貼文內容
            console.log(textContent.textContent) // 貼文內容
            var mediaContent = post.querySelector('div.x1xmf6yo'); // 貼文媒體
            if (mediaContent){
                var imgs = mediaContent.querySelectorAll('img');
                imgs.forEach((img) => {
                    console.log(img.src); // 貼文媒體
                })
            }
        }
    })
})()