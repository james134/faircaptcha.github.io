var express = require('express');
var app = express();
var path = require('path');

app.use(express.urlencoded({extended: true}));
app.use(express.json());

app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/register', function(request, response){
    response.header("Access-Control-Allow-Origin", "*");
    response.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    let kv = "";
    for (const key in request.body) {  
       kv += (key+" : "+request.body[key]+"\n")
    }
    response.end(kv);
});



app.listen(process.env.PORT || 8080, function () {
    console.log('Node app is live!');
});