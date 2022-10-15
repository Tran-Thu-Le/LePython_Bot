from lepythonbot.bot import text_to_code, execute, format_md
from lepythonbot.token import get_token
import os
import discord
from lepythonbot.webserver import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} logged in now!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content
    sender = message.author.name

    print(f"User={sender} sent a message.")

    text_report = text_to_code(text)
    if text_report["end_process"]:
        if text_report["error"] != "":
            await message.channel.send(text_report["error"])
        # else:
        #     print("no error no code")
        #     pass
    else:

        report = execute(text_report["code"])

        if report["result"] != "":
            await message.channel.send(format_md(report["result"]))
        if report["error"] != "":
            await message.channel.send(format_md(report["error"]))
        if report["picture"] != "":
            try:
                # with open("lepythonbot/picture.png", 'rb') as fpicture:
                #     picture = discord.File(fpicture)
                #     await message.channel.send(file=picture)
                await message.channel.send(file=report["picture"])
            except Exception as err:
                print(err)
                print("could not send figure")

    print(f"User={sender} got result.")
    print("-"*20)


if __name__ == "__main__":
    my_secret = get_token()
    # my_secret = os.environ['TOKEN']
    # # see https://stackoverflow.com/questions/70920148/pycord-message-content-is-empty
    keep_alive()
    client.run(my_secret)
