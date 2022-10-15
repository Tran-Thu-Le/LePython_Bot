import os


def get_token():
    """
        return the hidden token
    """
    try:
        farther_folder = os.getcwd().split("/")[-2]
        if farther_folder == "github":
            from lepythonbot.hide import TOKEN
            token = TOKEN
        else:
            token = os.environ["TOKEN"]
        return token
    except:
        raise Exception(
            "Can not access Discord bot's token from local machine")
