const https = require('https');

var randomStrings = [];
const min_rand_str = 10;
const rand_str_batch = 100;
const rand_len = 20;

function refillRandomness(){
    req = https.request({
        hostname: 'www.random.org',
        port: 443,
        path: '/strings/?num=' + rand_str_batch + '&len=' + rand_len + '&digits=on&upperalpha=on&loweralpha=on&unique=on&format=plain&rnd=new',
        method: 'GET'
    }, res => {
        let all_chunks = [];
        res.on('data', chunk => {
            all_chunks.push(chunk);
        })
        res.on('end', () => {
            Buffer.concat(all_chunks).toString().split('\n').forEach(function(rand){
                if (rand.length==rand_len) {
                    randomStrings.push(rand);
                }
            })
        });
        res.on('error', (error) => {
            console.log(error.message);
        });
    })
    req.end()
}

function getRandomString(callback){
    let rand = randomStrings.shift();
    callback((typeof(rand) != "string"),  rand);

    if (randomStrings.length < min_rand_str) refillRandomness();
}

module.exports = { getRandomString }