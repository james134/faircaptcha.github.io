const crypto = require("crypto");
const email = require('./email');
const randomness = require('./randomness');
const { Pool, Client } = require('pg');
const pool = new Pool({
  connectionString: //process.env.PG_URI,
  "postgres://ilaggcwb:DjsdOCDePRbexGTyXkML_VJQXCIezwnl@lallah.db.elephantsql.com:5432/ilaggcwb"
})

function registerUser(request, response, rand){
    let addr = request.body.email.trim().toLowerCase();
    let api_key = crypto.createHash('md5').update(new Date().getTime() + addr).digest('hex');
    const text = 'INSERT INTO users.users(api_key, secret, signals, email) VALUES($1, $2, $3, $4) RETURNING api_key, secret'
    const values = [
        api_key,
        crypto.createHash('sha256').update(rand + api_key).digest('hex'),
        '{"'+ request.body.signals.join('","') +'"}',
        addr
    ]
    pool.query(text, values, (err, result) => {
        if (err) {
            response.end(err.stack);
        } else {
            email.sendActivation(addr, result.rows[0], response)
        }
        //pool.end()
    })
}

function buildTempKey(req, res){
    let api_key = req.query.key;
    var text = 'SELECT * FROM users.users WHERE api_key = $1'
    var values = [
        api_key
    ]
    pool.query(text, values, (err, result) => {
        if (err) {
            return res.sendStatus(500);
        }

        //create a temporary key
        getRandomString.getRandomString(function(err, rand){
            if(err){
                return res.sendStatus(500);
            }

            text = 'INSERT INTO users.temp_keys(temp_key, api_key) VALUES ($1, $2)'
            values = [
                rand,
                api_key
            ]
            pool.query(text, values, (err, result) => {
                if (err) {
                    return res.sendStatus(500);
                }
                
                email.sendActivation(addr, result.rows[0], response)
                //pool.end()
            })
        })
        email.sendActivation(addr, result.rows[0], response)
        //pool.end()
    })
}

module.exports = { registerUser, buildTempKey }