var fs = require('fs');
var server = require('http');

server.createServer(function(request, response) {
   // fs.readFile('view/index.html', function(err,data) {
        response.writeHead(200, {
            'Content-Type': 'text/html'
        });
        response.write("hello world");
        response.end();
   // });
}).listen(8080);
