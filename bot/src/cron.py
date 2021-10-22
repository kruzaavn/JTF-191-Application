import discord
import aiohttp
import os

token = os.getenv('DISCORD_TOKEN')
user = os.getenv('API_SERVER_USER')
password = os.getenv('API_SERVER_PASSWORD')

auth = aiohttp.BasicAuth(login=user, password=password)


class Client(discord.Client):

    async def on_ready(self):
        print('Scheduler is online', flush=True)