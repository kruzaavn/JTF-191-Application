import discord
import os
import aiohttp
import pprint
import emoji

token = os.getenv('DISCORD_TOKEN')
user = os.getenv('API_SERVER_USER')
password = os.getenv('API_SERVER_PASSWORD')

camera_emoji = emoji.emojize(":camera:")
supported_image_formats = ['jpg', 'jpeg', 'png', 'tiff', 'bmp']


class Client(discord.Client):

    async def on_ready(self):
        print('JP5 is online', flush=True)

    async def on_message(self, message):

        if self.is_attachment_image(message.attachments):
            await message.add_reaction(camera_emoji)

    async def on_raw_reaction_add(self, payload):

        if str(payload.emoji) == camera_emoji:
            await self.upload_image(payload)

    async def upload_image(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

    def is_attachment_image(self, attachment):

        if attachment:

            file_ext = attachment[0].filename.rsplit(".", 1)[-1]

            return file_ext in supported_image_formats


if __name__ == '__main__':

    client = Client()
    client.run(token)

