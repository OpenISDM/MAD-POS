//Debug module 'longjohn'
require('longjohn');
//We need http,querstring modules to build our post string
//We need fs module to save .json file in file system
var http = require('http');
var querystring = require('querystring');
var fs = require("fs");
//Read topicProfile.json
var outputFilepath = './Resource/topicProfile.json';

function registratoin() {
  // Bulid the post string from an object
  var postData = querystring.stringify({
    'posAddress': '台北市南港區研究院路二段128號',
    'LatLng': '25.13722,121.50096',
    'macAddress': 'FC-4D-D4-3A-D5-24'
  });

  // An object of options to indicate where to post to
  var postOptions = {
    hostname: '140.109.22.197',
    port: 80,
    path: '/whereAreURLs?latlng=25.13722,121.50096',
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

      fs.writeFile(outputFilepath, chunk, function(err) {
        if (err) {
          console.log(err);
        } else {
          console.log("JSON saved to " + outputFilepath);
        }
      });

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

exports.registratoin = registratoin;
