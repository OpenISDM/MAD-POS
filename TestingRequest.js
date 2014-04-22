require('longjohn');
var http = require('http');
var querystring = require('querystring');

var post_options = {
    hostname: '140.109.21.186',
    port: 80,
    path: '/hub/php/',
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
        //'Content-Length': post_data.length
    }
};

var post_data = querystring.stringify({
    'mode': 'subscribe',
    'topic': 'http://140.109.22.197/static/Topic/110091/110091.json',
    'callback': 'http://140.109.22.181/callback'

});

var req = http.request(post_options, function(res) {
    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    res.setEncoding('utf8');

    var responseString = '';

    res.on('data', function(chunk) {
        responseString += chunk;
        console.log('DATA-BODY:' + responseString);
    });
    /*res.on('end', function() {
        var resultobject = JSON.parse(responseString);
        console.log('DATA-END:' + resultobject);
    });*/
});

req.on('error', function(e) {
    console.log('problem with request: ' + e.message);
});

// write data to request body
//req.write('data\n');
console.log('POST-BODY:' + post_data);
req.write(post_data);
req.end();
