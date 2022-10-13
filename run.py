import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess

from tools import is_safe

BANNED_COMMANDS = ["os", "sys", "subprocess", "open", "exec", "eval", "ffmpeg"]


class Programme(object):

    def __init__(self, text):
        self.text = text
        self.bool_plt_show = False

    def execute(self):
        """
      0. check syntax in text 
      1. text --> raw_code 
      2. if raw_code is safe then continue otherwise return err
      3. raw_code --> code 
        3.1. if there is a 'plt.show' in code 
        the save fig to a file
      4. execute code save result to fout.txt and ferr.txt
        
    """
        if self._is_syntax_valid():
            raw_code = self._text_to_raw_code()
            if self._is_raw_code_safe():
                code = self._raw_code_to_code(raw_code)
                self._save_code(code)
                self._run_subprocess()  # save fout.txt, ferr.txt
                fout = None
                ferr = None
                ffig = None
                report = {
                    "output": None,
                    "error": "Invalid syntax. Try `/py`",
                    "figure": None
                }
                return report
        else:
            report = {
                "output": None,
                "error": "Invalid syntax. Try `/py`",
                "figure": None
            }
            return report

    def _is_syntax_valid(self):
        """
      /py 

      ```py
      ```
    """
        text = self.text

        # 1. message must start with `/py`
        flag_a = text.startswith("/py") or text.startswith("/lepython3")

        # 2. the code should be in ```py <code>```
        sentences = text.split("\n")
        ids = []
        for i in range(len(sentences)):
            # print(i, sentences[i])
            if sentences[i].startswith("```"):
                ids += [i]

        flag_b = len(ids) == 2

        if flag_a and flag_b:
            return True
        else:
            return False

    def _text_to_raw_code(self):
        """
      Modify text to raw_code
    """

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
