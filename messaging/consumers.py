import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread, Message
from django.contrib.auth.models import User
from datetime import datetime

''' Consumers for Asynchronous Messaging '''


class ChatConsumer(AsyncConsumer):

    # async prefix turns into async function
    async def websocket_connect(self, event):
        print("connected", event)
        # get users involved and thread, make chat room
        user = self.scope['user']
        other_user = self.scope['path'][13:-1]
        second_user = User.objects.get(username=other_user)
        thread_obj = await self.get_thread(user, second_user)
        self.thread_obj = thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive", event)
        # get message and user from
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict = json.loads(front_text)
            msg = loaded_dict.get('message')
            user = self.scope['user']
            new_event ={
                "message": msg,
                "username": user.username
            }
            # make message object
            await self.create_message(user,msg)
            # broadcast message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(new_event)
                }
            )

    async def chat_message(self, event):
        # send message to front end
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.get_or_new(self, user,other_username)

    # save to db, update thread timestamp
    @database_sync_to_async
    def create_message(self, user, msg):
        new_message = Message(thread=self.thread_obj, user=user, message=msg)
        new_message.save()
        self.thread_obj.timestamp = datetime.now()
        self.thread_obj.save()
