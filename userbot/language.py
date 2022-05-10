# © Copyright Brend Userbot 
# t.me/BrendOwner tərəfindən xəta düzəldilmişdir
# Baxıb öyrənərsən))

from . import LANGUAGE, LOGS, bot, PLUGIN_ID
from json import loads, JSONDecodeError
from os import path, remove
from telethon.tl.types import InputMessagesFilterDocument

pchannel = bot.get_entity(PLUGIN_ID)
LANGUAGE_JSON = None

for dil in bot.iter_messages(pchannel, filter=InputMessagesFilterDocument):
    if ((len(dil.file.name.split(".")) >= 2) and (dil.file.name.split(".")[1] == "brendjson")):
        if path.isfile(f"./userbot/language/{dil.file.name}"):
            try:
                LANGUAGE_JSON = loads(open(f"./userbot/language/{dil.file.name}", "r").read())
            except JSONDecodeError:
                dil.delete()
                remove(f"./userbot/language/{dil.file.name}")

                if path.isfile("./userbot/language/DEFAULT.brendjson"):
                    LOGS.warn("Defolt dil dil faylı istifadə olunur...")
                    LANGUAGE_JSON = loads(open(f"./userbot/language/DEFAULT.brendjson", "r").read())
                else:
                    raise Exception("Your language file is invalid")
        else:
            try:
                DOSYA = dil.download_media(file="./userbot/language/")
                LANGUAGE_JSON = loads(open(DOSYA, "r").read())
            except JSONDecodeError:
                dil.delete()
                if path.isfile("./userbot/language/DEFAULT.brendjson"):
                    LOGS.warn("Defolt dil faylı istifadə olunur...")
                    LANGUAGE_JSON = loads(open(f"./userbot/language/DEFAULT.brendjson", "r").read())
                else:
                    raise Exception("Your language file is invalid")
        break

if LANGUAGE_JSON == None:
    if path.isfile(f"./userbot/language/{LANGUAGE}.brendjson"):
        try:
            LANGUAGE_JSON = loads(open(f"./userbot/language/{LANGUAGE}.brendjson", "r").read())
        except JSONDecodeError:
            raise Exception("Invalid json file")
    else:
        if path.isfile("./userbot/language/DEFAULT.brendjson"):
            LOGS.warn("Default dil faylı istifadə olunur...")
            LANGUAGE_JSON = loads(open(f"./userbot/language/DEFAULT.brendjson", "r").read())
        else:
            raise Exception(f"Didn't find {LANGUAGE} file")

def get_value (plugin = None, value = None):
    global LANGUAGE_JSON

    if LANGUAGE_JSON == None:
        raise Exception("Please load language file first")
    else:
        if not plugin == None or value == None:
            Plugin = LANGUAGE_JSON.get("STRINGS").get(plugin)
            if Plugin == None:
                raise Exception("Invalid plugin")
            else:
                String = LANGUAGE_JSON.get("STRINGS").get(plugin).get(value)
                if String == None:
                    return Plugin
                else:
                    return String
        else:
            raise Exception("Invalid plugin or string")
