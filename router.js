function route(handle, pathname, response, postData, topicContent) {
  console.log("About to route a request for " + pathname);
  if (typeof handle[pathname] === 'function') {
    console.log('route==topicContent=====: ' + topicContent);
    handle[pathname](response, postData, topicContent);
  } else {
    console.log("No request handler found for " + pathname);
    response.writeHead(404, {
      "Content-Type": "text/plain"
    });
    response.write("404 Not found");
    response.end();
  }
}

exports.route = route;
