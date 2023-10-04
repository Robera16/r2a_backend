WebSockets Message Sampple payload

Request :point_right: ```
{
  "message_type": "text",
  "message": "Helo There Message",
  "room_id": 8
}
```

Response :point_right: ```{
  "type": "send_to_websocket",
  "message_type": "text",
  "message": "From user sudha",
  "sender": "sudha",
  "room_id": 8,
  "created": "18 Jun 2020 17:46:49 UTC"
}
```

[Client for testing sockets](https://chrome.google.com/webstore/detail/websocket-king-client/cbcbkhdmedgianpaifchdaddpnmgnknn?hl=en)



1. Websocket url starts with ws://<url>/
2. for messages we need to pass group id pathvariable and bearer='<actual_bearer>' as params

## EndPoints List :ledger:
1. /channel/group_chat/<room_id>/?bearer=ActualBearerHere....
