# Modul Tam olaraq Brend Userbot a məxsusdur
# Copyright Brend Userbot
# @BrendOwner

import re, os, importlib, userbot.cmdhelp
from telethon.tl.types import InputMessagesFilterDocument
from userbot import CMD_HELP, bot, tgbot, PLUGIN_ID, PATTERNS
from userbot.events import register
from userbot.main import extractCommands
from userbot.language import get_value
LANG = get_value("__plugin")


@register(outgoing=True, pattern="^.plist")
async def plist(event):
    if PLUGIN_ID != None:
        await event.edit(LANG["PLIST_CHECKING"])
        yuklenen = f"{LANG['PLIST']}\n\n"
        async for plugin in event.client.iter_messages(PLUGIN_ID, filter=InputMessagesFilterDocument):
            try:
                fayladi = plugin.file.name.split(".")[1]
            except:
                continue
            if fayladi == "py":
                yuklenen += f"⚡ {plugin.file.name}\n"
        await event.edit(yuklenen)
    else:
        await event.edit(LANG["TEMP_PLUGIN"])

@register(outgoing=True, pattern="^.pinstall")
async def pins(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
    else:
        await event.edit(LANG["REPLY_TO_FILE"])
        return
    await event.edit(LANG["DOWNLOADING"])
    fayl = await event.client.download_media(reply_message, "./userbot/modules/")  
    try:
        spec = importlib.util.spec_from_file_location(fayl, fayl)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"{LANG['PLUGIN_BUGGED']} {e}`")
        return os.remove("./userbot/modules/" + fayl)
    fayll = open(fayl, "r").read()
    if re.search(r"@tgbot\.on\(.*pattern=(r|)\".*\".*\)", fayll):
        emr = re.findall(r"\(.*pattern=(r|)\"(.*)\".*\)", fayll)
        emrler = ""
        i = 0
        while i < len(emrr):
            komut = emrr[i][1]
            CMD_HELP["tgbot_" + emr] = f"{LANG['PLUGIN_DESC']} {emr}"
            emrler += emr + " "
            i += 1
        await event.edit(LANG['PLUGIN_DOWNLOADED'] % emrler)
    else:
        Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", fayll)
        if (not type(Pattern) == list) or (len(Pattern) < 1 or len(Pattern[0]) < 1):
            if re.search(r'CmdHelp\(.*\)', fayll):
                fayladi = reply_message.file.name.replace('.py', '')
                extractCommands(dosya)
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", fayll)[0]
                await reply_message.forward_to(PLUGIN_ID)
                return await event.edit(f'**📂 {fayladi} Modulu Yükləndi!**\n⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗\n**ℹ️ Info:** `.brend {cmdhelp}`')
            else:
                await reply_message.forward_to(PLUGIN_ID)
                userbot.cmdhelp.CmdHelp(fayl).add_warning('❌Əmr Tapılmadı!').add()
                return await event.edit(LANG['PLUGIN_DESCLESS'])
        else:
            if re.search(r'CmdHelp\(.*\)', fayll):
                fayladi = reply_message.file.name.replace('.py', '')
                extractCommands(fayl)
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", fayll)[0]
                await reply_message.forward_to(PLUGIN_ID)
                return await event.edit(f'**📂 {fayladi} Modulu Yükləndi!**\n⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗\n**ℹ️ Info:** `.brend {cmdhelp}`')
            else:
                fayladi = reply_message.file.name.replace('.py', '')
                extractCommands(dosya)
                await reply_message.forward_to(PLUGIN_ID)
                return await event.edit(f'**📂 {fayladi} Modulu Yükləndi!**\n⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗\n**ℹ️ Info:** `.brend {fayladi}`')

@register(outgoing=True, pattern="^.premove ?(.*)")
async def premove(event):
    modul = event.pattern_match.group(1).lower()
    if len(modul) < 1:
        await event.edit(LANG['PREMOVE_GIVE_NAME'])
        return
    await event.edit(LANG['PREMOVE_DELETING'])
    i = 0
    a = 0
    async for message in event.client.iter_messages(PLUGIN_ID, filter=InputMessagesFilterDocument, search=modul):
        await message.delete()
        try:
            os.remove(f"./userbot/modules/{message.file.name}")
        except FileNotFoundError:
            await event.reply(LANG['ALREADY_DELETED'])
        i += 1
        if i > 1:
            break
    if i == 0:
        await event.edit(LANG['NOT_FOUND_PLUGIN'])
    else:
        await event.edit(LANG['PLUG_DELETED'])

@register(outgoing=True, pattern="^.psend ?(.*)")
async def psend(event):
    modul = event.pattern_match.group(1)
    if len(modul) < 1:
        await event.edit(LANG['PREMOVE_GIVE_NAME'])
        return
    if os.path.isfile(f"./userbot/modules/{modul}.py"):
        await event.client.send_file(event.chat_id, f"./userbot/modules/{modul}.py", caption=LANG['BREND_PLUGIN_CAPTION'])
        await event.delete()
    else:
        await event.edit(LANG['NOT_FOUND_PLUGIN'])


@register(outgoing=True, pattern="^.ptest")
async def ptest(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
    else:
        await event.edit(LANG["REPLY_TO_FILE"])
        return
    await event.edit(LANG["DOWNLOADING"])
    if not os.path.exists('./userbot/temp_plugins/'):
        os.makedirs('./userbot/temp_plugins')
    fayl = await event.client.download_media(reply_message, "./userbot/temp_plugins/") 
    try:
        spec = importlib.util.spec_from_file_location(fayl, fayl)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"{LANG['PLUGIN_BUGGED']} {e}`")
        return os.remove("./userbot/temp_plugins/" + fayl)
    fayladi = reply_message.file.name.replace('.py', '')
    return await event.edit(f'**☑️ {fayladi} Plugin Test Üçün Yükləndi!**\n⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗⋖⋗\n🆘 Userbotu yenidən başlatdığınızda modul silinmiş olacaq.')
