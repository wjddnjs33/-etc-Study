const express = require("express");
const app = express();

app.get('/', (req, res) => {
    res.setHeader('Content-disposition', 'attachment;filename=result.json');
	res.end('Hi')
});

app.get('/a', (req, res) => {
	res.end('Hi')
});

app.listen(3000, () => {
	console.log("http://141.164.52.207:3000");
});