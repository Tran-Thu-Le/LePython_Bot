import os
from webserver import keep_alive
import discord
from tools import execute

intents = discord.Intents.all()
client = discord.Client(intents=intents)
# see https://stackoverflow.com/questions/70920148/pycord-message-content-is-empty


@client.event
async def on_ready():
    print(f"{client.user} logged in now!")


@client.event
async def on_message(message):
    if message.content.startswith("/lepython3") or message.content.startswith(
            "/py"):
        print("main2.py is running")
        #1. work with result
        print(
            f"User={message.author.name} requests for executing Python3 code.")
        out, bool_plt_show = execute(message.content)
        deco = "**Result:**\n"
        out = "```\n" + out + "\n```"
        await message.channel.send(deco + out)

        # 2. work with figure
        if bool_plt_show:
            with open("myfig.png", 'rb') as f:
                picture = discord.File(f)
            await message.channel.send(file=picture)

        try:
            print(f"User={message.author.name} got the results.")
            print("-" * 20)
        except:
            print("error here")


# keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)

