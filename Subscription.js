//Debug module 'longjohn'
require('longjohn');
//We need this to build our post string
var http = require('http');
var querystring = require('querystring');

// Bulid the post string from an object
var postData = querystring.stringify({
  'mode': 'subscribe',
  'topic': 'http://140.109.22.197/static/Topic/110091/110091.json',
  'callback': 'http://140.109.22.181/callback'
});

// An object of options to indicate where to post to
var postOptions = {
  hostname: '140.109.21.186',
  port: 80,
  path: '/hub/php/',
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': postData.length
  }
};

// Set up the request
var req = http.request(postOptions, function(res) {

  console.log('STATUS: ' + res.statusCode);
  console.log('HEADERS: ' + JSON.stringify(res.headers));
  
  res.setEncoding('utf8');
  res.on('data', function onData(chunk) {
    console.log('DATA: ' + chunk);
  });
});

req.on('error', function onError(e) {
  console.log('Problem with request: ' + e.message);
});

// write data to request body
// POST the data
// console.log('POST-BODY:' + postData);
req.write(postData);
req.end();
