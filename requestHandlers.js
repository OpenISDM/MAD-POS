function root(response, postData) {
  console.log("Request handler 'root' was called.");
  response.writeHead(200, {
    "Content-Type": "text/plain"
  });
  response.write("Hello this root Page");
  response.end();
}

function callbackURL(response, postData) {
  console.log("Request handler 'callbackURL' was called.");
  response.writeHead(200, {
    "Content-Type": "text/plain"
  });
  response.write("Hello callbackURL\n" + "You've sent: \n" + postData);
  response.end();
}

function download(response, postData) {
  console.log("Request handler 'callbackURL' was called.");
  response.writeHead(200, {
    "Content-Type": "text/plain"
  });
  response.write("Hello callbackURL\n" + "You've sent: \n" + postData);
  response.end();
}


exports.root = root;
exports.callbackURL = callbackURL;
exports.download = download;
