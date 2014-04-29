var fs = require("fs");
var url = require('url');
var jsonData = '';
var requestHandlers = require("./topicProfile.json");

// An object of options to indicate where to post to
var postOptions = {
  port: 80,
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '203'
  }
};
postOptions['hostname'] = url.parse(requestHandlers.hub_url).host;
postOptions['port'] = 80;
postOptions['path'] = url.parse(requestHandlers.hub_url).pathname;

console.log('postOptions: ' + postOptions.hostname);
console.log('postOptions: ' + postOptions.port);
console.log('postOptions: ' + postOptions.path);
console.log('postOptions: ' + postOptions.method);
