import json


def loadFileConfig():
    with open("config.json") as f:
        data = json.load(f)
    return data

dataConfig = loadFileConfig()



