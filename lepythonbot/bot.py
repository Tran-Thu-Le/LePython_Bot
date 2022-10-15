import subprocess
import os
import discord

BANNED_COMMANDS = [
    " os", " sys", " subprocess", " open(", "exec(", " eval(", " ffmpeg", "savefig("
]


def format_md(result):
    lines = ["**Result:**",
             "```",
             result,
             "```"]
    return "\n".join(lines)


def text_to_code(text):
    report = {
        # "result": "",
        "error": "",
        # "picture": "",  # discord.File() accepts str
        "end_process": False,
        "code": ""
    }

    # print(text)
    # print("-"*10)
    # print(text[:3])
    # print("-"*10)

    # 1. invalid call --> stop
    if text.startswith("/py") or text.startswith("/lepython3"):
        pass
    else:
        report["end_process"] = True
        print("No request")
        return report

    # 2. invalid format --> stop
    sentences = text.split("\n")
    ids = []
    for i in range(len(sentences)):
        # print(i, sentences[i])
        if sentences[i].startswith("```"):
            ids += [i]

    if len(ids) == 1 or len(ids) > 2:
        report["error"] = "Invalid code. Python code should be placed in between\n```py\n<code>\n```"
        report["end_process"] = True
        print(report["error"])
        return report
    elif len(ids) == 0:
        report["end_process"] = True
        print("No request")
        return report

    # 3. export raw code
    raw_code = "\n".join(sentences[ids[0]+1: ids[1]])
    # print(raw_code)
    # print("-"*10)

    # 4. raw code is unsafe --> stop
    for word in BANNED_COMMANDS:
        if word in raw_code:
            report["error"] = "Due to security reason, the following commands are banned: os, sys, subprocess, open, exec, eval, ffmpeg, savefig. Please remove them and try again!"
            report["end_process"] = True
            print(report["error"])
            return report

    # 5. if there is .show( (plt.show) in
    if "plt.show()" in raw_code:
        pre_code = [
            "# deactive plt.show() by 'Agg'",
            "import matplotlib",
            "matplotlib.use('Agg')"
        ]
        pre_code = "\n".join(pre_code)
        code = pre_code + "\n" + raw_code.replace("plt.show()",
                                                  "plt.savefig('lepythonbot/picture.png')")
    else:
        code = raw_code

    report["code"] = code
    # report["end_process"] = False
    # print("`"*3 + "REAL CODE")
    # print(code)
    # print("`"*3)
    return report


def execute(code):

    # 0. innit report
    report = {
        "result": "",
        "error": "",
        "picture": "",  # discord.File() accepts str
        # "end_process": False,
    }

    # 1. run code
    with open("lepythonbot/result.txt", 'w+') as fresult:
        with open("lepythonbot/error.txt", "w+") as ferror:
            with open("code.py", "w+") as fcode:

                fcode.write(code)

            # subprocess should be outside of fcode's block
            # could not run the matplotlib package code.py if it is inside lepythonbot
            subprocess.call(["python", "code.py"],
                            stdout=fresult,
                            stderr=ferror)
            # result = fresult.read()
            # error = ferror.read()
            # print("pass here")
            # print(result)
            # print(error)

    with open("lepythonbot/result.txt") as fresult:
        report["result"] = fresult.read()
    with open("lepythonbot/error.txt") as ferror:
        report["error"] = ferror.read()

    if report["result"] != "":
        print("code is executed without error")
    if report["error"] != "":
        print(report["error"])

    os.remove("lepythonbot/result.txt")
    os.remove("lepythonbot/error.txt")
    os.remove("code.py")

    # print("*"*10)
    # print(report["result"], "...")
    # print(report["error"], "...")

    # 2. figure
    if "plt.savefig('lepythonbot/picture.png')" in code:
        print("a figure has been saved")
        with open("lepythonbot/picture.png", 'rb') as fpicture:
            report["picture"] = discord.File(fpicture)
        os.remove("lepythonbot/picture.png")

    # report["end_process"] = True

    return report
