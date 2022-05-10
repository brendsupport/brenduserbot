from userbot.cmdhelp import CmdHelp
from userbot import PLUGIN_ID, CMD_HELP
from userbot.events import register
from re import search
from json import loads, JSONDecodeError
from userbot.language import LANGUAGE_JSON
from os import remove

@register(outgoing=True, pattern="^.dil ?(.*)")
@register(outgoing=True, pattern="^.lang ?(.*)")
async def dil(event):
    global LANGUAGE_JSON
    emr = event.pattern_match.group(1)
    if search(r"install", emr):
        await event.edit("`Dil faylı yüklənir... Xaiş Edirik Gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            fayl = await reply.download_media()
            if ((len(reply.file.name.split(".")) >= 2) and (not reply.file.name.split(".")[1] == "brendjson")):
                return await event.edit("`Xaiş edirik etibarlı` **BrendJSON** `faylı verin!`")
            try:
                fayl = loads(open(fayl, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xaiş edirik etibarlı` **BrendJSON** `faylı verin!`")
            await event.edit(f"`{fayl['LANGUAGE']}` `dili yükleniyor...`")
            pchannel = await event.client.get_entity(PLUGIN_ID)
            fayl = await reply.download_media(file="./userbot/language/")
            fayl = loads(open(fayl, "r").read())
            await reply.forward_to(pchannel)
            LANGUAGE_JSON = fayl
            await event.edit(f"✅ `{fayl['LANGUAGE']}` `dili  müvəffəqiyyətlə yükləndi!`\n\n**Dəyişikliklətin yaddaşa yazılması üçün botu yenidən başladın!**")
        else:
            await event.edit("**Zəhmət olmasa bir dil faylına cavab verin!**")
    elif search(r"info", emr):
        await event.edit("`Dil faylı məlumatları gətirilir... Xaiş edirik Gözləyin.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            if ((len(reply.file.name.split(".")) >= 1) and (not reply.file.name.split(".")[1] == "brendjson")):
                return await event.edit("`Xaiş edirik etibarlı` **BrendJSON** `faylı verin!`")
            fayl = await reply.download_media()
            try:
                fayl = loads(open(fayl, "r").read())
            except JSONDecodeError:
                return await event.edit("`Xaiş edirik etibarlı` **BrendJSON** `faylı verin!`")
            await event.edit(
                f"**Dil: **`{fayl['LANGUAGE']}`\n"
                f"**Dil Kodu: **`{fayl['LANGCODE']}`\n"
                f"**Tərcüməçi: **`{fayl['AUTHOR']}`\n"
                f"\n\n`Dil faylını yükləmək üçün` `.dil install` `əmrindən istifadə edin.`"
            )
        else:
            await event.edit("**Hansısa bir dil faylına cavab verin!**")
    else:
        await event.edit(
            f"**Dil: **`{LANGUAGE_JSON['LANGUAGE']}`\n"
            f"**Dil Kodu: **`{LANGUAGE_JSON['LANGCODE']}`\n"
            f"**Tərcüməçi: **`{LANGUAGE_JSON ['AUTHOR']}`\n"
            f"\n\nBaşqa dillər üçün @BrendDil kanalına baxa bilərsiniz."
        )

CmdHelp('lang').add_command(
    'lang', None, 'Yüklədiyiniz dil haqqında məlumat verir.'
).add_command(
    'lang info', '<cavablamaq>', 'Cavab verdiyiniz dil faylı haqqında məlumat verər.'
).add_command(
    'lang install', '<cavablamaq>', 'Cavab verdiyiniz dil faylını yükləyir.'
).add()
