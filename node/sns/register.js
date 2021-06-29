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

// Register Page
router.get('/register', (req, res) => {
    console.log("Register");
    res.render('register.ejs');
});

// Register Logic
router.post('/register', (req, res) => {
    name = req.body.name
    id = req.body.id
    pw = req.body.pw
    rpw = req.body.rpw

    if(name == '' || id == '' || pw == '' || rpw == ''){
        res.send("<script>alert('빈 값이 존재하면 안 됩니다.');history.go(-1);</script>");
    }
    else{
        query = "SELECT * FROM users WHERE id = '" + id + "'";
        func.getuser(query, function(err, data){
            if(err){
                console.log("Error : ", err);
                res.send(err);
            }
            else{
              if(data){
                  res.send("<script>alert('이미 사용 중인 아이디입니다.');history.go(-1);</script>");
              }
              else{
                if(pw !== rpw){
                    res.send("<script>alert('동일한 비밀번호를 입력해주세요.');history.go(-1);</script>");
                }
                else{
                    params = [name, id, func.sha256(pw), 'null', '0', '0'];
                    querys = mysql.format("insert into users(name, id, pw, D, image, Following, Followers) values(?, ?, ?, NOW(), ?, ?, ?);", params);
                    //query = "insert into users(name, id, pw, D) values('" + name + "', '" + id + "', '" + sha256(pw) + "', NOW())";
                    conn.query(querys, function(err, rows){
                        if(err) { res.send(err);}
                        else {res.redirect("/login");}
                    });
                }
              }
            }
        });
     }
});

module.exports = router;