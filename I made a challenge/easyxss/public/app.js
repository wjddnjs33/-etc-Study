// 넣을 파일이 없어서 .. 

const express = require('express');
const request = require('request');
const { chromium } = require('playwright');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT;

async function bot(url) {
    const browser = await chromium.launch();
    const context = await browser.newContext();
    const cookies = fs.readFileSync('cookies.json', 'utf8');

    const deserializedCookies = JSON.parse(cookies)
    await context.addCookies([deserializedCookies]);

    const page = await context.newPage()
    await page.goto(url)

    setTimeout(() => {
        try {
            browser.close();
        } catch (err) {
            console.log(`err : ${err}`);
        }
    }, 15000);
}

app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

app.use(express.urlencoded({extended: false}));
app.use(express.static(__dirname + '/static'));

app.get('/', (req, res) => {
    res.render('index.html')
});

app.get('/report', (req, res) => {
    res.render('report.html')
})

app.post('/report', (req, res) => {
    const url = req.body.url;
    try{
        const protocol = url.split(':')[0]
        if (protocol == 'http' || protocol == 'https'){
            bot(url);
            res.send(url)
        } else {
            res.send('<script>alert("An unacceptable protocol detected");history.go(-1);</script>')
        }
    } catch (err) {
        res.send('<script>alert("Internal Server Error!");history.go(-1);</script>')
    }
});

app.listen(PORT, () => {
    console.log('good');
});