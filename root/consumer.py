from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer 
from json import dumps, loads
from ADMIN.models import chat_list
from customer.models import C8Message,ActiveUser


from django.core.signals import request_started

class ChatRoom(AsyncWebsocketConsumer):
    #  ---------------👇 DB CONNECTION WITH WEB SOCKET 👇-----------------

    @database_sync_to_async
    def get_profile(self):
        user_profile = self.scope["user"].get_profile
        context = {
            'name':self.scope["user"].username,
            'pk':user_profile.pk,
            'img':user_profile.profile_photo.url
        }
        return context

    @database_sync_to_async
    def set_user_active_status(self):
        user_profile = self.scope["user"].get_profile
        ActiveUser.objects.filter(profile=user_profile).update(is_active=True)
        return user_profile

    @database_sync_to_async
    def set_user_offline_status(self):
        user_profile = self.scope["user"].get_profile
        ActiveUser.objects.filter(profile=user_profile).update(is_active=False)
        return user_profile

    @database_sync_to_async
    def is_superUser(self):
        user = self.scope["user"]
        if user.is_superuser:
            return True
        return False


    @database_sync_to_async
    def check_auth(self):
        user_pk = self.scope["user"].get_profile.pk
        try:
            roomId = int(self.scope["url_route"]["kwargs"]["room_id"])
        except ValueError:
            roomId = None
        return roomId == user_pk

    @database_sync_to_async
    def store_message(self,message):
         C8Message.objects.create(
            roomId=self.room_name,
            profile= self.scope["user"].get_profile,
            message=message
        )
    
       
    @database_sync_to_async
    def reload_admin_c8List(self):
        if self.is_superUser():
            
            obj = chat_list.objects.filter(admin_profile=self.scope["user"].get_profile)
            if obj.exists():
                data = loads(obj[0].lists).get("clist")
                roomId = int(self.scope["url_route"]["kwargs"]["room_id"])
                try:
                    data.remove(roomId)
                except:
                    pass
                new_data = [roomId] + data
                
                print(new_data)
                

                obj.update(lists=dumps({'clist':new_data}))
                    
            
    
        
    
       
        



    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        if await self.check_auth() or await self.is_superUser():
            print("#################################################")

            print(await self.check_auth())
            print(self.room_name)

            print(await self.is_superUser())

            # set user status to offline 👇😍
            await self.set_user_active_status()

            
            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            # await self.channel_layer.group_send(
            #     self.room_group_name,
            #     {
            #         "type":"broadcast_message",
            #         # "message":"HEllow world"
            #     }
            # )

    async def broadcast_message(self,event):
        message = event["message"]
        
        await self.send(text_data=dumps({
            "message":message
        }))

    
    async def receive(self, text_data):
        message = loads(text_data)

        message = message["message"]
        await self.store_message(message)
        await self.reload_admin_c8List()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chatroom_message",
                "message": message,
                "client":await self.get_profile()
            }
        )
    
    async def chatroom_message(self,event):
         message = event["message"]
  
         await self.send(text_data=dumps({
            "message":message,
            'client':event['client']
         }))


    
    async def disconnect(self, close_code):

        if await self.check_auth() or await self.is_superUser():
            
            # set user status to offline 👇
            await self.set_user_offline_status()
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )


class adminAlert(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_profile(self):
        user_profile = self.scope["user"].get_profile.pk
        return user_profile

    @database_sync_to_async
    def is_superuser(self):
        return self.scope["user"].is_superuser
    

    async def connect(self):
            self.room_name = "admin_alert"
  
            self.room_group_name = f"chat_{self.room_name}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def receive(self, text_data):

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chatroom_message",
                "alert": True,
                'id': await self.get_profile()
            }
        )

    async def chatroom_message(self,event):
        if await self.is_superuser():
            await self.send(text_data=dumps({
                    "alert": True,
                    'id': event['id']
            }))
        else:
            await self.close()
      
    async def disconnect(self, close_code):

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

