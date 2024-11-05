// server.js
const express = require('express');
const path = require('path');
const fs = require('fs').promises;
const app = express();

// 設定靜態檔案目錄
app.use(express.static('public'));
app.use('/comics', express.static('comic'));

// 取得所有漫畫類別
app.get('/api/categories', async (req, res) => {
    try {
        const categories = await fs.readdir('comic');
        res.json(categories);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 取得特定漫畫的所有章節
app.get('/api/chapters/:category', async (req, res) => {
    try {
        const chapters = await fs.readdir(path.join('comic', req.params.category));
        res.json(chapters.sort((a, b) => parseInt(a) - parseInt(b)));
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 取得特定章節的所有圖片
app.get('/api/images/:category/:chapter', async (req, res) => {
    try {
        const images = await fs.readdir(
            path.join('comic', req.params.category, req.params.chapter)
        );
        const imageList = images
            .filter(file => file.toLowerCase().endsWith('.jpg'))
            .sort((a, b) => {
                const numA = parseInt(a.match(/\d+/)?.[0] || 0);
                const numB = parseInt(b.match(/\d+/)?.[0] || 0);
                return numA - numB;
            });
        res.json(imageList);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
