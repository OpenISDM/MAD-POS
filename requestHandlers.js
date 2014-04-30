var fs = require('fs');
var outputFilepath = './topicContent.json';

function root(response, postData) {
  console.log("Request handler 'root' was called.");
  response.writeHead(200, {
    "Content-Type": "text/plain"
  });
  response.write("Hello this root Page");
  response.end();
}

function callback(response, postData) {
  console.log("Request handler 'callbackURL' was called.");
  fs.writeFile(outputFilepath, postData, function(err) {
    if (err) {
      console.log(err);
    } else {
      console.log("JSON saved to " + outputFilepath);
    }
  });
  response.writeHead(200, {
    "Content-Type": "text/plain"
  });
  response.write("Hello callbackURL\n" + "You've sent: \n" + postData);
  response.end();
}

function topic(response, postData) {
  console.log("Request handler 'download' was called.");
  fs.readFile("./topicContent.json", "binary", function(error, file) {
    if (error) {
      response.writeHead(500, {
        "Content-Type": "text/plain"
      });
      response.write(error + "\n");
      response.end();
    } else {
      response.writeHead(200, {
        "Content-Type": "text/json"
      });
      response.write(file, "binary");
      response.end();
    }
  });
}

function image(response, postData) {
  console.log("Request handler 'image' was called.");
  fs.readFile("./TWN-112-583552.png", "binary", function(error, file) {
    if (error) {
      response.writeHead(500, {
        "Content-Type": "text/plain"
      });
      response.write(error + "\n");
      response.end();
    } else {
      response.writeHead(200, {
        "Content-Type": "image/png"
      });
      response.write(file, "binary");
      response.end();
    }
  });
}


exports.root = root;
exports.callback = callback;
exports.topic = topic;
exports.image = image;
