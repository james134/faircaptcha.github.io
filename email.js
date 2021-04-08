const nodemailer = require('nodemailer');
const transport = nodemailer.createTransport({
    pool: true,
    host: "smtp.yandex.ru",
    port: 465,
    secure: true, // use TLS
    auth: {
       user: 'faircaptcha@sense.africa',
       pass: 'ftzyggqafavrddqx'
    }
});

function sendActivation(address, row, response){
    transport.sendMail({
        from: 'faircaptcha@sense.africa',
        to: address, // List of recipients
        subject: 'Your FairCAPTCHA credentials',
        text: JSON.stringify(row),
        html: '<h1>Your fairCAPTCHA credentials</h1><p>' + JSON.stringify(row) +'</p>'
    }, function(err, info) {
        if (err) {
            row.email_status = "FAIL - unable to send credentials"
        } else {
            row.email_status = "OK - credentials queued for delivery to "+address
        }
        response.end(JSON.stringify(rows));
    });
}

module.exports = { sendActivation }