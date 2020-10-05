const express = require('express');
const crypto = require("crypto");
const path = require('path');
const { Pool, Client } = require('pg');

var app = express();
const pool = new Pool({
  connectionString: process.env.PG_URI,
})

app.use(express.urlencoded({extended: true}));
app.use(express.json());

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/register', function(request, response){
    //POST keys: email,endpoint,signals
    response.header("Access-Control-Allow-Origin", "*");
    response.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    const email_regex = /\S+@\S+\.\S+/;

    if ("email" in request.body
        && email_regex.test(request.body.email)
        && "signals" in request.body) {
        let now = new Date().getTime();
        const text = 'INSERT INTO users(api_key, secret, signals, email) VALUES($1, $2, $3, $4) RETURNING *'
        const values = [
            crypto.createHash('md5').update(now + email).digest('hex'),
            crypto.createHash('sha256').update(now + email).digest('hex'),
            "'{\""+ request.body.signals.split(',').join('","') +"\"}'",
            request.body.email.trim().toLowerCase()
        ]
        try{
            pool.query(text, values, (err, res) => {
                if (err) {
                    console.log(err.stack)
                    response.end(err.stack)
                } else {
                    console.log(res.rows[0])
                    response.end(res.rows[0])
                }
                //pool.end()
            })
        }
        catch(err){
            console.log(err.message);
            response.end(err.message);
        }
    } else response.end("");
});


app.listen(process.env.PORT || 8080, function () {
    console.log('Node app is live!');
});