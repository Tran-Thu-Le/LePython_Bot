import os


def get_token():
    """
        return the hidden token
    """
    try:
        farther_folder = os.getcwd().split("/")[-2]
        if farther_folder == "projects":
            from lepythonbot.hidden_token import TOKEN
            token = TOKEN
        else:
            token = os.environ["TOKEN"]
        return token
    except:
        raise Exception(
            "Can not access Discord bot's token from local machine")
