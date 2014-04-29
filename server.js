var http = require("http");
var url = require("url");
var querystring = require("querystring");

function start(route, handle) {
  function onRequest(request, response) {
    var postData = "";
    var pathname = url.parse(request.url).pathname;
    console.log("Request for " + pathname + " received.");

    request.setEncoding("utf8");

    if (request.method == 'POST') {

      request.addListener("data", function data(postDataChunk) {
        postData += postDataChunk;
        console.log("Received POST data chunk '" +
          postDataChunk + "'.");
      });
      request.addListener("end", function end() {

        var objectPostData = querystring.parse(postData);
        for (var i in objectPostData) {
          console.log('After parse: ' + objectPostData[i]);
        }
        route(handle, pathname, response, postData);
      });

    } else {
      route(handle, pathname, response);
    }
  }

  http.createServer(onRequest).listen(8888);
  console.log('Server has started and running on port ' + 8888);
}

exports.start = start;
