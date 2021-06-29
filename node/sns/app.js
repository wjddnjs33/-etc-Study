const express = require('express');
const app = express();

const register = require('./register');
const loginout = require("./loginout");
const main = require("./main");
const admin = require("./admin");

// router setting
app.use(loginout);
app.use(register);
app.use(main);
app.use(admin);

app.listen(3000, () => {
    console.log("Listeing PORT 3000....");
});
