# kurier
A cross-platform GUI client for testing AMQP-based APIs

This application was written for my needs in developing and testing AMQP-based microservices, that will behave like the Postman application. For example, I'm using it for development microservices in the [Open Matchmaking](https://github.com/OpenMatchmaking) project.

# Features
- Postman-like client, but for using with AMQP-based APIs
- Validating queues, exchanges and routing keys for existing in the virtual host
- Saving and restoring valid requests from the history
- Search old requests in the history by the request exchange and the routing key

# Screenshots
<img src="https://github.com/Relrin/kurier/blob/master/screenshots/windows-app.png" width="400"> | <img src="https://github.com/Relrin/kurier/blob/master/screenshots/mac-app.png" width="425">
:----------------------------------------------------------------------------:|:-------------------------:
  Windows                                                                     | Mac OS X 

# License
The kurier project is published under BSD license. For more details read the [LICENSE](https://github.com/Relrin/kurier/blob/master/LICENSE) file.
