const express = require("express");
const jwt = require('jsonwebtoken');
const mysql = require('mysql');
const cookieParser = require('cookie-parser');
const func = require("./userfunc");

const router = express();
const conn = func.connection()

router.set('views', __dirname + '/template');
router.set('view engine', 'ejs');

router.use(cookieParser());
router.use(express.urlencoded({extended: true}));

const SECRET = "20011202";

router.get('/login', (req, res) => {
    res.render('login.ejs');
});

// Login Logic
router.post('/login', (req, res) => {
    id = req.body.id;
    pw = req.body.pw;

    query = mysql.format("SELECT * FROM users where id = ?", id);
    func.getuser(query, function(err, data){
        if(err){
            console.log("Error : ", err)
        }
        else{
            if(data){
                 if(func.sha256(pw) !== data.pw){ res.send("<script>alert('아이디 혹은 비밀번호가 일치하지 않습니다.');history.go(-1);</script>");}
                 else{
                     const token = jwt.sign({ user: data.id}, SECRET, { expiresIn: '1h'});
                     res.cookie('user', token);
                     res.redirect("/");
                 }
            }
            else { res.send("<script>alert('아이디 혹은 비밀번호가 일치하지 않습니다.');history.go(-1);</script>")}
        }
    });
});

// Logout Logic
router.get('/logout', (req, res) => {
    res.clearCookie("user");
    res.redirect("/");
});

module.exports = router;