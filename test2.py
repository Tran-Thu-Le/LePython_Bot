from lepythonbot.bot import text_to_code, execute


def discord_sim(text, user):
    print("------ Discord simulation is activating")
    text_report = text_to_code(text)
    if text_report["end_process"]:
        if text_report["error"] != "":
            print("LePythonBot sent error!")
        else:
            print("no error no code")
            pass
    else:
        report = execute(text_report["code"])

        if report["result"] != "":
            print(report["result"])
            print("LePythonBot sent result!")
        if report["error"] != "":
            print(report["error"])
            print("LePythonBot sent error!")
        if report["picture"] != "":
            print(report["picture"])
            print("LePythonBot sent picture!")

        # print("end process here")

    print("------ Discord simulation is done")


TEXT_err1 = """/py 

"""

TEXT_err2 = """/py 
```
"""


TEXT_err3 = """/py 
```
import os
print("rose")
```
"""

TEXT1 = """/py 
```py
print("Hello from TEXT1")
print("rose")
```
"""

TEXT2 = """/py 
```py
print("Hello from TEXT2")
import numpy as np 
# a = np.arange(1, 10)
# print(a**2)
```
"""

TEXT3_err = """/py 
```py
print("Hello from TEXT3")
import numpy as np 
import matplotlib.pyplot as plt 
a = np.linspace(0, 10, 100)
b = np.sin(a)
plt.plot(a, b)
plt.show()
```
"""

TEXT4_err = """/py 
```py
import matplotlib 
```
"""

if __name__ == "__main__":
    # discord_sim(text=TEXT_err3, user="Le")
    discord_sim(text=TEXT3_err, user="Le")
