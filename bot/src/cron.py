import discord
import aiohttp
import os
from datetime import datetime
from pytz import timezone

token = os.getenv('DISCORD_TOKEN')
user = os.getenv('API_SERVER_USER')
password = os.getenv('API_SERVER_PASSWORD')
time_zone = timezone(os.getenv('TIMEZONE', 'US/Eastern'))

auth = aiohttp.BasicAuth(login=user, password=password)

dt_format = '%Y-%m-%dT%H:%M:%S%z'


class Event:

    def __init__(self, **kwargs):

        self.start = datetime.strptime(kwargs.get('start'), dt_format).astimezone(time_zone)
        self.end = datetime.strptime(kwargs.get('start'), dt_format).astimezone(time_zone)
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.squadrons = kwargs.get('required_squadrons')

    def __repr__(self):
        return f'{self.type}:{self.name}'

    def __str__(self):
        return self.__repr__()

    def discord_message(self):

        return f"""{self.type.upper()}: {self.name} @ {self.start.strftime('%H:%M')} {time_zone}"""


class Client(discord.Client):

    def __init__(self):
        super().__init__()
        self.now = self.get_now_localized_datetime()

    async def on_ready(self):
        print('Scheduler is online', flush=True)
        print(f'{datetime.strftime(self.now, dt_format)}, TZ:{self.now.tzinfo}')
        events = await self.get_schedule()

        if events:

            await self.get_general_channel().send(f"Today's scheduled events, for more info see https://jtf191.com/#/schedule")

        for event in events:

            print(f"Reminding {event.discord_message()}")

            if event.squadrons:
                await self.send_event_to_squadron_channels(event)

            await self.send_event_to_general_channel(event)

        await self.close()

    async def get_schedule(self):

        async with aiohttp.ClientSession(auth=auth) as session:

            async with session.get(f'http://api-server:8000/api/roster/event/list/') as r:
                response_message = await r.json()

                if r.ok:
                    events = [Event(**x) for x in response_message]
                    events = list(filter(lambda x: x.start.date() == self.now.date(), events))
                    events.sort(key=lambda x: x.start)
                    return events

                else:
                    print(response_message)

    async def send_event_to_squadron_channels(self, event):

        required_channels = {x['discord_channel'] for x in event.squadrons if x['discord_channel'] is not None}

        squadron_channels = list(filter(lambda x: x.name in required_channels, self.get_all_channels()))

        for channel in squadron_channels:

            await channel.send(event.discord_message())

    async def send_event_to_general_channel(self, event):

        await self.get_general_channel().send(event.discord_message())

    def get_general_channel(self):
        return [x for x in self.get_all_channels() if x.name == 'general-chat'][0]

    @staticmethod
    def get_now_localized_datetime(tz=time_zone):
        return datetime.now(time_zone)


if __name__ == '__main__':

    client = Client()
    client.run(token)
