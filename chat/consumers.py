# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from .models                    import *
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        Room.objects.create(name=self.room_name).delete()

        # Rejoindre le groupe de discussion
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de discussion
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data): # Recevoir les messages du client
        text_data_json = json.loads(text_data)
        message  = text_data_json['message']
        username = text_data_json['username']

        room = Room.objects.get(self.room_name)
        GroupMessage.objects.create(
            room=room,
            author=username,
            content=message
        ).save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        ) # Envoyer le message à tous les autres clients dans le groupe

    # Recevoir les messages des autres clients et les envoyer au client actuel
    async def chat_message(self, event):
        message  = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

class ChatPrivateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Rejoindre le groupe de discussion
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de discussion
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recevoir les messages du client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']

        # Enregistrer le message privé dans la base de données
        PrivateMessage.objects.create(
            sender=self.scope['user'],
            receiver=User.objects.get(username=receiver),
            content=message
        ).save()

        # Envoyer le message aux deux utilisateurs concernés
        await self.channel_layer.group_send(
            f'private_chat_{self.scope["user"].username}_{receiver}',
            {
                'type': 'private_chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver
            }
        )
        await self.channel_layer.group_send(
            f'private_chat_{receiver}_{self.scope["user"].username}',
            {
                'type': 'private_chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver
            }
        )

    # Recevoir les messages privés des autres clients et les envoyer aux clients concernés
    async def private_chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver
        }))
