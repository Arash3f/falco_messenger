
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from messenger.models import GroupChat , Message
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.user = self.scope['user']
        self.slug = self.scope['url_route']['kwargs']['slug']
        self.chat = await self.get_chat()
        self.chat_room_id = f"chat_{self.slug}"

        if self.chat:
            await self.channel_layer.group_add(
                self.chat_room_id,
                self.channel_name
            )
            await self.accept()

        else:

            await self.close()

    @database_sync_to_async
    def get_chat(self):
        try:
            chat = GroupChat.objects.get(slug=self.slug)
            return chat
        except GroupChat.DoesNotExist:
            return None
    
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.chat_room_id,
            self.channel_name
        )

    async def receive(self,text_data=None , bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            text = text_data_json['text']

            await self.create_message(text)

            await self.channel_layer.group_send(
                self.chat_room_id,{
                    'type':'chat_message' , 
                    'message': json.dumps({'type':"msg", 'sender':self.user.username, 'text':text }),
                    'sender_channel_name':self.channel_name
                }
            )
            
    @database_sync_to_async
    def create_message(self, text):
        Message.objects.create(chat_id=self.chat.id, author_id=self.user.id, body=text)
    
    async def chat_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data= message)

    async def chat_message_warning(self, event):
        message = event['message']
        await self.send(text_data= message)



