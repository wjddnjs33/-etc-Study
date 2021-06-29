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
router.use(express.json());

// User Information : admin panel
router.get('/users', (req, res) => {
    let query = "SELECT * FROM users";
    conn.query(query, function(err, rows, fields){
        if(err) console.log('query is not excuted, select fail...\n' + err);
        else res.render('admin_users.ejs', {list : rows});
    });
});

// User Information Update
router.get('/update', (req, res) => {
    let query = "SELECT * FROM users WHERE _id = 1";
    conn.query(query, function(err, rows, fileds){
        if(err) console.log('query is not excuted, select fail...\n' + err);
        //else console.log(rows[0].id);
        else res.render('admin_update.ejs', {list : rows});
    });
});

router.post('/update', (req, res) => {
    console.log(req.body);
    query = mysql.format("DELETE FROM users WHERE num = ?", req.body.id);
    console.log(query);
    conn.query(query, function(err, rows){
        console.log(rows);
        if(err){
                console.log("query is not excute, Delete Fail...\n" + err);
        }else{
                console.log("Success");
        }
    });
});

module.exports = router;
