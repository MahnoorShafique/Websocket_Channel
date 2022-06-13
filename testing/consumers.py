import asyncio
from time import sleep

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
import json


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.room_group_name)
        self.accept()
        #  for sending data from backend/serve to /clientfrontend use send
        self.send(text_data=json.dumps({'status': 'connected fghtny'}))

    """ for sending data from frontend to backend use receive function"""

    def recieve(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status': 'we got you'}))

    def disconnect(self, *arg, **kwarg):
        print("disconnected")

    def send_notification(self, event):
        print("send notification")
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({'payload': data}))
        print("send notification")


# when client sends request to server it gets blocked until receive response from server.
class MySyncConsumer(SyncConsumer):
    """This handler is called
        when client initially opens
        a connection and is about
        to finish the web socket handshake
    """

    # all these methods are handlers so an events must be associated with them
    def websocket_connect(self, event):
        print("connected")
        print("channel_layer",self.channel_layer)# get defaut channel layer
        print("Channel Name: ",self.channel_name) # get default channel name
        # group_add is method of asynConsumer so to use it with syn with have to convert it
        # add channel to group
        async_to_sync(self.channel_layer.group_Add)('programmers',self.channel_name)

        # when client sends a connection request .server has to accept/reject it. when it accept request so following send is called.
        self.send({
            'type': 'websocket.accept'
        })


    def websocket_receive(self, event):
        """this handler is called when data received from client"""

        print("received", event)
        # the text below is that sent by client to server(client to server)
        print("received", event['text'])
        # txt in send method is that one, sent by server to client(server to client)
        async_to_sync(self.channel_layer.group_send)('programmers',{
            # client ko bhjne k leye type use kr rhy hn.
            'type':'chat.message',# chat.message is an event we will write chat_message handler for it
            'message':event['text']
        }
                                        )

        for i in range(5):
            self.send({'type': 'websocket.send',
                       'text': json.dumps({'count': i})
                      # 'text': "from server"+ str(i) # text here only takes string so if we have to dend a dictionary to client we have to use .dump method.

                       })

            sleep(1)

    def chat_message(self, event):
        print('event...', event)
        print('Actual Data...', event['text'])
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def websocket_disconnect(self, event):
        """when connection to client is either
           lost or closed from either client or sever"""
        print("disconnected", event)
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # Discarding Group
        self.channel_layer.group_discard('programmers',self.channel_name)
        raise StopConsumer()


# in Async clients can perform other tasks rather getting blocked and waiting for servers response.
class MyASyncConsumer(AsyncConsumer):
    """This handler is called
        when client initially opens
        a connection and is about
        to finish the web socket handshake
    ”"""

    async def websocket_Connect(self, event):
        print("connected2", event)
        await self.send({'type': 'websocket.accept'

        })
        await asyncio.sleep(1)

    async def websocket_receive(self, event):
        """this handler is called when data
     received from client"""
        print("received2", event)
        for i in range(50):
             await self.send({'type': 'websocket.send',
                       'text': "from server" + str(i)})


    async def websocket_disconnect(self, event):
        """when connection to client is either
           lost or closed from either client or sever"""
        print("disconnected2", event)
        raise StopConsumer()
