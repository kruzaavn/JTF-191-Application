import discord
import aiohttp
import os
from datetime import datetime

token = os.getenv('DISCORD_TOKEN')
user = os.getenv('API_SERVER_USER')
password = os.getenv('API_SERVER_PASSWORD')

auth = aiohttp.BasicAuth(login=user, password=password)


class Client(discord.Client):

    async def on_ready(self):
        print('Scheduler is online', flush=True)
        events = await self.get_schedule()
        print(events)
        print(list(self.get_all_channels()))
        await self.close()

    async def get_schedule(self):

        async with aiohttp.ClientSession(auth=auth) as session:

            async with session.get(f'http://api-server:8000/api/roster/event/list/') as r:
                response_message = await r.json()

                if r.ok:
                    return [x for x in response_message if
                            datetime.strptime(x['start'], '%Y-%m-%dT%H:%M:%S%z').date() == datetime.today().date()]
                else:
                    print(response_message)

    async def message_event(self, event):
        pass


if __name__ == '__main__':

    client = Client()
    client.run(token)
