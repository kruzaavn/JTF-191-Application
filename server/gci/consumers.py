from channels.generic.websocket import AsyncWebsocketConsumer


class GCIConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'gci'

        await self.channel_layer.group_add()


    async def receive(self, text_data=None, bytes_data=None):
        await self.send(text_data=text_data)

