import os
from telethon.tl.types import InputMessagesFilterDocument
from userbot.events import register
from userbot import BOT_USERNAME, PATTERNS, CMD_HELP, PLUGIN_CHANNEL_ID
import userbot.cmdhelp
from random import choice, sample
import importlib
import re
from userbot.main import extractCommands

from userbot.language import get_value
LANG = get_value("__plugin")

@register(outgoing=True, pattern="^.store ?(.*)")
@register(outgoing=True, pattern="^.ma[gğ]aza ?(.*)")
async def magaza(event):
    plugin = event.pattern_match.group(1)
    await event.edit('**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n`🔎 Plugin\'i axtarıram... Biraz gözlə.`')
    split = plugin.split()
    if plugin == '':
        plugin = 'Son Yüklənən'
        plugins = await event.client.get_messages('@brendplugin', limit=15, filter=InputMessagesFilterDocument)
    elif len(split) >= 1 and (split[0] == 'random' or split[0] == 'rastgele'):
        plugin = 'Təsadüfi'
        plugins = await event.client.get_messages('@brendplugin', limit=None, filter=InputMessagesFilterDocument)
        plugins = sample(plugins, int(split[1]) if len(split) == 2 else 5)
    else:
        plugins = await event.client.get_messages('@brendplugin', limit=None, search=plugin, filter=InputMessagesFilterDocument)
        random = await event.client.get_messages('@brendplugin', limit=None, filter=InputMessagesFilterDocument)
        random = choice(random)
        random_file = random.file.name

    result = f'**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n**🔎 Arama:** `{plugin}`\n**🔢 Nəticələr: __({len(plugins)})__**\n➖➖➖➖➖\n\n'
    
    if len(plugins) == 0:
        result += f'**Heç nə tapa bilmədim...**\n`{random_file}` __plugininə nə deyirsən?__'
    else:
        for plugin in plugins:
            plugin_lines = plugin.raw_text.splitlines()
            result += f'**⬇️ {plugin_lines[0]}** `({plugin.file.name})`**:** '
            if len(plugin_lines[2]) < 50:
                result += f'__{plugin_lines[2]}__'
            else:
                result += f'__{plugin_lines[2][:50]}...__'
            result += f'\n**ℹ️ Yükləmək üçübn:** `{PATTERNS[:1]}sinstall {plugin.id}`\n➖➖➖➖➖\n'
    return await event.edit(result)

# Plugin Mağazası
@register(outgoing=True, pattern="^.sy[üu]kl[eə] ?(.*)")
@register(outgoing=True, pattern="^.sinstall ?(.*)")
async def sinstall(event):
    plugin = event.pattern_match.group(1)
    try:
        plugin = int(plugin)
    except:
        return await event.edit('**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n**⚠️ Xəta:** `Xahiş edirəm yalnız nömrələr yazın. Eklentiləri axtarmaq istəyirsinizsə .store əmrini istifadə edin.`')
    
    await event.edit('**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n`🔎 Plugin\'i gətirirəm... Zəhmət olmasa gözlə.`')
    plugin = await event.client.get_messages('@brendplugin', ids=plugin)
    await event.edit(f'**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n`✅ {plugin.file.name} plugin gətirildi!`\n`⬇️ Plugini yükləyirəm... Zəhmət olmasa gözlə.`')
    dosya = await plugin.download_media('./userbot/modules/')
    await event.edit(f'**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n`✅ {plugin.file.name} indirme başarılı!`\n`⬇️ Plugini yüklüyürəm... Zəhmət olmasa gözlə.`')
    
    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        os.remove("./userbot/modules/" + dosya)
        return await event.edit(f'**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n**⚠️ Xəta:** `xətaliı. {e}`\n**BUNU ADMINLƏRƏ BİLDİRİN!**')

    dosy = open(dosya, "r").read()
    if re.search(r"@tgbot\.on\(.*pattern=(r|)\".*\".*\)", dosy):
        komu = re.findall(r"\(.*pattern=(r|)\"(.*)\".*\)", dosy)
        komutlar = ""
        i = 0
        while i < len(komu):
            komut = komu[i][1]
            CMD_HELP["tgbot_" + komut] = f"{LANG['PLUGIN_DESC']} {komut}"
            komutlar += komut + " "
            i += 1
        await event.edit(LANG['PLUGIN_DOWNLOADED'] % komutlar)
    else:
        Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", dosy)

        if (not type(Pattern) == list) or (len(Pattern) < 1 or len(Pattern[0]) < 1):
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'**Modül yükləndi!**\n__Modulun əmrləri və istifadəsi haqqında məlumat əldə etmək__ `.brend {cmdhelp}` __yazın.__')
            else:
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                userbot.cmdhelp.CmdHelp(dosya).add_warning('Komutlar bulunamadı!').add()
                return await event.edit(LANG['PLUGIN_DESCLESS'])
        else:
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n**✅ Modül yükləndi!**\n__Modulun əmrləri və istifadəsi haqqında məlumat əldə etmək__ `.brend {cmdhelp}` __yazın.__')
            else:
                dosyaAdi = plugin.file.name.replace('.py', '')
                extractCommands(dosya)
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'**Brend Plugin Mağazası**\n__Versiyon 1.0__\n\n**✅ *Modül yükləndi!**\n__ℹ️ Modulun əmrləri və istifadəsi haqqında məlumat əldə etmək__ `.brend {dosyaAdi}` __yazın.__')

userbot.cmdhelp.CmdHelp('store').add_command(
    'store', '<söz>', 'Ən son Pluginləri Plugin kanalına gətirir. Sözlər yazsanız, axtarar.'
).add_command(
    'store random', '<sayı>', 'Pluginden kanalından təsadüfi plaginlər əldə edir.', 'store random 10'
).add_command(
    'sinstall', '<sayı>', 'Plugini birbaşa Plugin kanalından yükləyir.'
).add()
