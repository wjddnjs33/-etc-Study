const express = require("express");
const mysql = require('mysql');
const func = require("./userfunc");
const jwt = require('jsonwebtoken');

const conn = func.connection();
const router = express();

router.set('views', __dirname + '/template');
router.set('view engine', 'ejs');

const SECRET = "20011202";

// main page
router.get('/',(req, res) => {
    console.log("Success");
    if(req.cookies['user'] !== undefined){
        try{
            JWT = req.cookies['user'];
            decoded = jwt.verify(JWT, SECRET);
            if (decoded){
            query = mysql.format("select * from post; select * from users where id = ?", decoded['user']); 
		    conn.query(query, function(err, result){
			    res.render("index_.ejs", {users:result[1],data:result[0]});
		    });
            } else{
                res.clearCookie("user");
                res.status(401).json({ error: 'unauthorized'});
            }
        } catch (err){
            res.clearCookie("user");
            res.status(401).json({ error: 'unauthorized' });
        }
    }
    else{
	    query = "select * from post"
	    conn.query(query, function(err, result){
		    res.render("index.ejs", {data:result});
	    });
    }
});

module.exports = router;