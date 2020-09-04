var express = require('express');
var app = express();
//var path = require('path');

app.use(express.urlencoded({extended: true}));
app.use(express.json());

app.post('/register', function(request, response){
    console.log("reg");
    response.header("Access-Control-Allow-Origin", "*");
    response.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    console.log(request.body)
    for (const key in request.body) {  
        console.log(key+" : "+request.body[key])
    }
});

/*
app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});
*/

app.listen(process.env.PORT || 8080, function () {
    console.log('Node app is live!');
});