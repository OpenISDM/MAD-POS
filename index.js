var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");
var Subscription = require("./Subscription");
var Registration = require("./Registration");

var handle = {}
handle["/"] = requestHandlers.root;
handle["/callback"] = requestHandlers.callback;
handle["/topic"] = requestHandlers.topic;
handle["/image"] = requestHandlers.image;

server.start(router.route, handle);
Registration.registratoin();
Subscription.subscription();