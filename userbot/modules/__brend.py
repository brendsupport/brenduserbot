# Copyright Brend Userbot
# Bu modul Brend Userbota Məxsusdur

from userbot import CMD_HELP
from userbot.events import register
from userbot.language import get_value
LANG = get_value("__brend")

@register(outgoing=True, pattern="^.brend(?: |$)(.*)")
async def brend(event):
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(LANG["NEED_PLUGIN"])
    else:
        string = ""
        sehife = [sorted(list(CMD_HELP))[i:i + 5] for i in range(0, len(sorted(list(CMD_HELP))), 5)]
        for i in sehife:
            string += f'⚡ '
            for sira, a in enumerate(i):
                string += "`" + str(a)
                if sira == i.index(i[-1]):
                    string += "`"
                else:
                    string += "`, "
            string += "\n"
        await event.edit(LANG["NEED_PLUGIN"] + '\n\n' + string)
