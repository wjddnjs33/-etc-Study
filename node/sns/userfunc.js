// mysql connection or user check

const mysql = require("mysql");
const dbconfig = require("./config/db.js");
const conn = dbconfig.init();
exports.connection = function() {
    return dbconfig.init();
}

exports.getuser = function (sql, callback){
    conn.query(sql, function (err, rows){
        if(err)
          callback(err, null);
        else
          callback(null, rows[0]);
    });
}
////////////////////////////////////////////////////////////////////////////

// password enc
const crypto = require("crypto");
exports.sha256 = function (data) {
    return crypto.createHash("sha256").update(data, "binary").digest("hex");
}
