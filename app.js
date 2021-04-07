const express = require('express');
const path = require('path');
const randomness = require('./randomness');
const database = require('./database');

var app = express();

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
        randomness.getRandomString(function(err, rand){
            if (err){
                response.end("Generating random numbers. Try again later.");
            }
            else database.registerUser(request, response, rand);
        })

    } else response.end("");
});

app.get('/min.js', function (req, res) {
    //?key=XXX
    if (typeof(req.query.key) != 'string') {
        res.sendStatus(400);
    }
    else database.buildTempKey(req, res);
});


app.listen(process.env.PORT || 8080, function () {
    console.log('Node app is live!');
});