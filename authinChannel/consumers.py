import json

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from pyasn1.debug import scope

from dbinChnl.models import Group, Chat


class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("connected")
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # groupName=self.scope['url_route']['kwargs']['groupName']
        self.groupName = self.scope['url_route']['kwargs']['groupName']

        async_to_sync(self.channel_layer.group_add)(self.groupName, self.channel_name)
        data={'type': 'websocket.accept'}
        data['result']={"abc"}
        self.send(data)

    def websocket_receive(self, event):
        """this handler is called when data received from client"""

        print("received", event)
        print("received", event['text'])
        print(" type received", type(event['text']))
        # data=json.loads(event['text'])
        try:

            data=event['text']
            groupName = self.scope['url_route']['kwargs']['groupName']
            group=Group.objects.filter(name=groupName).first()
            chats=[]
            if group:
                chats=Chat.objects.filter(group=group)
            else:
                group=Group(name=self.groupName)
                group.save()

            group = Group.objects.get(name=group)
            chat=Chat(
                content= data,       #data['msg'],
                group=group
            )
            chat.save()
        except Exception as e:
            return str(e)
        async_to_sync(self.channel_layer.group_send)(self.groupName, {# client ko bhjne k leye type use kr rhy hn.
            'type': 'chat.message',  # chat.message is an event we will write chat_message handler for it
            'message': event['text']})
            # 'message':chats})

    def chat_message(self, event):
        print('event...', event)
        print('Actual Data...',event['message'])
        self.send({'type': 'websocket.send', 'text': event['message']})

    def websocket_disconnect(self, event):
        print("disconnected", event)
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # Discarding Group
        # groupName = self.scope['url_route']['kwargs']['groupName']
        async_to_sync(self.channel_layer.group_discard)(self.groupName, self.channel_name)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected")
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        groupName = self.scope['url_route']['kwargs']['groupName']
        await self.channel_layer.group_add(groupName, self.channel_name)
        await self.send({'type': 'websocket.accept'})

    async def websocket_receive(self, event):
        """this handler is called when data received from client"""

        print("received", event)
        # the text below is that sent by client to server(client to server)
        print("received", event['text'])
        groupName = self.scope['url_route']['kwargs']['groupName']
        await self.channel_layer.group_send(groupName, {# client ko bhjne k leye type use kr rhy hn.
            'type': 'chat.message',  # chat.message is an event we will write chat_message handler for it
            'message': event['text']})

    async def chat_message(self, event):
        print('event...', event)
        print('Actual Data...', event['message'])
        await self.send({'type': 'websocket.send', 'text': event['message']})

    async def websocket_disconnect(self, event):

        print("disconnected", event)
        print("channel_layer", self.channel_layer)  # get defaut channel layer
        print("Channel Name: ", self.channel_name)  # get default channel name
        # Discarding Group
        groupName = self.scope['url_route']['kwargs']['groupName']
        await self.channel_layer.group_discard(groupName, self.channel_name)
        raise StopConsumer()
