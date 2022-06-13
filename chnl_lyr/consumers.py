from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from pyasn1.debug import scope


class MySyncConsumer(SyncConsumer):
    """This handler is called
        when client initially opens
        a connection and is about
        to finish the web socket handshake
    """

    # all these methods are handlers so an events must be associated with them
    def websocket_connect(self, event):
        print("connected")
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # group_add is method of asynConsumer so to use it with syn with have to convert it
        # add channel to group
        groupName=self.scope['url_route']['kwargs']['groupName']
        async_to_sync(self.channel_layer.group_add)(groupName, self.channel_name)

        # when client sends a connection request .server has to accept/reject it. when it accept request so following send is called.
        self.send({'type': 'websocket.accept'})

    def websocket_receive(self, event):
        """this handler is called when data received from client"""

        print("received", event)
        # the text below is that sent by client to server(client to server)
        print("received", event['text'])
        # txt in send method is that one, sent by server to client(server to client)
        # sending msg in group.
        groupName = self.scope['url_route']['kwargs']['groupName']
        async_to_sync(self.channel_layer.group_send)(groupName, {# client ko bhjne k leye type use kr rhy hn.
            'type': 'chat.message',  # chat.message is an event we will write chat_message handler for it
            'message': event['text']})

    def chat_message(self, event):
        print('event...', event)
        print('Actual Data...', event['message'])
        self.send({'type': 'websocket.send', 'text': event['message']})

    def websocket_disconnect(self, event):
        """when connection to client is either
           lost or closed from either client or sever"""
        print("disconnected", event)
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # Discarding Group
        groupName = self.scope['url_route']['kwargs']['groupName']
        async_to_sync(self.channel_layer.group_discard)(groupName, self.channel_name)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    """This handler is called
        when client initially opens
        a connection and is about
        to finish the web socket handshake
    """

    # all these methods are handlers so an events must be associated with them
    async def websocket_connect(self, event):
        print("connected")
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # group_add is method of asynConsumer so to use it with syn with have to convert it
        # add channel to group
        groupName = self.scope['url_route']['kwargs']['groupName']
        await self.channel_layer.group_add(groupName, self.channel_name)

        # when client sends a connection request .server has to accept/reject it. when it accept request so following send is called.
        await self.send({'type': 'websocket.accept'})

    async def websocket_receive(self, event):
        """this handler is called when data received from client"""

        print("received", event)
        # the text below is that sent by client to server(client to server)
        print("received", event['text'])
        # txt in send method is that one, sent by server to client(server to client)
        # sending msg in group.
        groupName = self.scope['url_route']['kwargs']['groupName']
        await self.channel_layer.group_send(groupName, {# client ko bhjne k leye type use kr rhy hn.
            'type': 'chat.message',  # chat.message is an event we will write chat_message handler for it
            'message': event['text']})

    async def chat_message(self, event):
        print('event...', event)
        print('Actual Data...', event['message'])
        await self.send({'type': 'websocket.send', 'text': event['message']})

    async def websocket_disconnect(self, event):
        """when connection to client is either
           lost or closed from either client or sever"""
        print("disconnected", event)
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # Discarding Group
        groupName = self.scope['url_route']['kwargs']['groupName']
        await self.channel_layer.group_discard(groupName, self.channel_name)
        raise StopConsumer()
