import discord
import os

token = os.getenv('DISCORD_TOKEN')


class Client(discord.Client):

    pass


if __name__ == '__main__':

    client = Client()
    client.run(token)

