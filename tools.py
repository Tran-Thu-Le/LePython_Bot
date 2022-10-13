import subprocess
import os
# import matplotlib.pyplot as plt

ALLOWED_PACKAGES = ["numpy", "matplotlib", "scipy", "pandas"]
BANNED_COMMANDS = [
    " os", " sys", " subprocess", " open", "exec", " eval", " ffmpeg"
]


def is_safe(code):
    """
    prevent package os, sys
    prevent plt.show()
  """
    # text
    try:
        if "os " in code or " os" in code:
            raise Exception(
                "Due to security reason, 'os' package is not allowed!\nPlease remove it and try again!"
            )
        if "sys " in code or " sys" in code:
            raise Exception(
                "Due to security reason, 'sys' package is not allowed!\nPlease remove it and try again!"
            )

        # if "plt.show" in code:
        #   raise Exception(
        #     "plt.show() is not allowed for now!\nPlease remove it and try again!")
        return True
    except Exception as err:
        with open('ferr.txt', "w+") as ferr:
            ferr.write(str(err))


def is_safe_2(code):
    """
    Banned packages/commands: os, sys, subprocess, open, exec, eval, ffmpeg
  """
    # text
    # print(code)
    # print("-" * 20)
    try:
        sentences = code.split("\n")
        for i in range(len(sentences)):
            for w in BANNED_COMMANDS:
                if w in sentences[i]:
                    raise Exception(
                        f"Line {i} command `{w}` is using!\n\n" +
                        "Due to security reason, the following commands are banned: os, sys, subprocess, open, exec, eval, ffmpeg. Please remove them and try again!"
                    )
        return True
    except Exception as err:
        with open('ferr.txt', "w+") as ferr:
            ferr.write(str(err))


def text_to_code(text):
    """
    process text to code
  """
    sentences = text.split("\n")
    python_script = []
    ids = []
    for i in range(len(sentences)):
        # print(i, sentences[i])
        if sentences[i].startswith("```"):
            ids += [i]

    if not len(ids) == 2:
        return "", False  #code, bool_plt_show

    for i in range(ids[0] + 1, ids[1]):
        # print(i, sentences[i])
        python_script += [sentences[i]]

    code = "\n".join(python_script)

    # extra processing
    bool_plt_show = False
    if "plt.show()" in code:
        bool_plt_show = True
        pre_code = [
            "# deactive plt.show() by 'Agg'", "import matplotlib",
            "matplotlib.use('Agg')"
        ]
        pre_code = "\n".join(pre_code)
        code = pre_code + "\n" + code.replace("plt.show()",
                                              "plt.savefig('myfig.png')")
    return code, bool_plt_show


def execute(text):
    code, bool_plt_show = text_to_code(text)
    # print(code)
    # print("-" * 20)

    # if is_safe(code):
    if is_safe_2(code):
        # print("... is_safe_2 function is running")
        with open('fout.txt', 'w+') as fout:
            with open("ferr.txt", "w+") as ferr:
                with open("code.py", "w+") as f:
                    f.write(code)
                subprocess.call(["python", "code.py"],
                                stdout=fout,
                                stderr=ferr)
        with open('fout.txt') as fout:
            out = fout.read()
        with open('ferr.txt') as ferr:
            err = ferr.read()
        return out + err, bool_plt_show

    else:
        # if the code is not safe,
        # the err has been saved into ferr.txt
        # so we just need to return the content of ferr.txt
        with open('ferr.txt') as ferr:
            err = ferr.read()
        return err, bool_plt_show
