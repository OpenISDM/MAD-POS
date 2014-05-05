//Debug module 'longjohn'
// require('longjohn');
//We need http,querstring modules to build our post string
//We need fs module to save .json file in file system
var http = require('http');
var querystring = require('querystring');
var fs = require('fs');
var url = require('url');
var topicProfile = require("./Resource/topicProfile.json");

function subscription() {
  // Bulid the post string from an object
  var postData = querystring.stringify({
    'mode': 'subscribe',
    'topic': topicProfile.topic_url,
    'callback': 'http://140.109.22.181/callback'
  });

  // An object of options to indicate where to post to
  var postOptions = {
    port: 80,
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Content-Length': postData.length
    }
  };
  postOptions['hostname'] = url.parse(topicProfile.hub_url).host;
  postOptions['path'] = url.parse(topicProfile.hub_url).pathname;
  /*
TO DO a function for automatic create object. or to judge port is Null or entiy.
*/

  // Set up the request
  var req = http.request(postOptions, function(res) {

    console.log('STATUS: ' + res.statusCode);
    console.log('HEADERS: ' + JSON.stringify(res.headers));
    console.dir('postOptions: ' + postOptions);

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
  console.log('POST-BODY:' + postData);
  req.write(postData);
  req.end();
}
exports.subscription = subscription;
