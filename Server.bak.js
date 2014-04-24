var fs = require('fs');
var server = require('http');

server.createServer(function(request, response) {
  fs.readFile('Mobile_Web_App/index.html', function(err, data) {
    response.writeHead(200, {
      'Content-Type': 'text/html'
    });
    response.write(data);
    response.end();
  });
}).listen(8080);
console.log('Server running on port ' + 8080);
