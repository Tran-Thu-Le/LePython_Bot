from tools import execute, text_to_code

# print(execute(text))
# print(text_to_code(text))


def discord_sim(text, user):
    print("------ Discord simulation is activating")
    if text.startswith("/lepython3") or text.startswith("/py"):

        #1. work with result
        print(f"User={user} requests for executing Python3 code.")
        out, bool_plt_show = execute(text)
        deco = "**Result:**\n"
        out = "```\n" + out + "\n```"
        print(deco + out)

        # 2. work with figure
        if bool_plt_show:
            # with open("myfig.png", 'rb') as f:
            #     picture = discord.File(f)
            # await message.channel.send(file=picture)
            print("Figure sent")

        print(f"User={user} got the results.")
        print("-" * 20)
        print("------ Discord simulation is done")


with open("text.txt", "r") as f:
    text = f.read()
discord_sim(text=text, user="Le")
