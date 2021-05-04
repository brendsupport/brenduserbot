import re
import userbot.modules.sql_helper.mesaj_sql as sql
from userbot import CMD_HELP
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR, ORJ_PLUGIN_MESAJLAR, PLUGIN_CHANNEL_ID
from userbot.cmdhelp import CmdHelp


from userbot.language import get_value
LANG = get_value("degistir")
@register(outgoing=True, pattern="^.editl[eə] ?(.*)")
@register(outgoing=True, pattern="^.d[eə]yi[sş]dir ?(.*)")
async def degistir(event):
    plugin = event.pattern_match.group(1)
    mesaj = re.search(r"\"(.*)\"", plugin)

    if mesaj:
        rege = re.findall(r"(?:|$)(.*)\"(.*)\"", plugin)
        plugin = rege[0][0]
        mesaj = rege[0][1]
    else:
        mesaj = []

    plugin = plugin.strip()
    TURLER = ["afk", "alive", "pm", "kickme", "dızcı", "ban", "mute", "approve", "disapprove", "block"]
    if type(mesaj) == list:
        if plugin in TURLER:
            if event.is_reply:
                reply = await event.get_reply_message()
                if reply.media:
                    mesaj = await reply.forward_to(PLUGIN_CHANNEL_ID)
                    PLUGIN_MESAJLAR[plugin] = reply
                    sql.ekle_mesaj(plugin, f"MEDYA_{mesaj.id}")
                    return await event.edit(f"Plugin(`{plugin}`) {LANG['SETTED_MEDIA']}")
                PLUGIN_MESAJLAR[plugin] = reply.text
                sql.ekle_mesaj(plugin, reply.text)
                return await event.edit(f"Plugin(`{plugin}`) {LANG['SETTED_REPLY']}")   

            silme = sql.sil_mesaj(plugin)
            if silme == True:
                PLUGIN_MESAJLAR[plugin] = ORJ_PLUGIN_MESAJLAR[plugin]
                await event.edit(LANG['SUCCESS_DELETED'])
            else:
                await event.edit(f"{LANG['ERROR_DELETED']}: `{silme}`")
        else:
            await event.edit(LANG['NOT_FOUND'] + ":`afk/alive/pm/kickme/dızcı/ban/mute/approve/disapprove/block`")
    elif len(plugin) < 1:
        await event.edit(LANG['USAGE'])
    elif type(mesaj) == str:
        if plugin in TURLER:
            if mesaj.isspace():
                await event.edit(LANG['CANNOT_EMPTY'])
                return
            else:
                PLUGIN_MESAJLAR[plugin] = mesaj
                sql.ekle_mesaj(plugin, mesaj)
                await event.edit(LANG['SETTED'].format(plu=plugin, msj=mesaj))
        else:
            await event.edit(LANG['NOT_FOUND'] + ":`afk/alive/pm/kickme/dızcı/ban/mute/approve/disapprove/block`")

CmdHelp('degistir').add_command(
    'deyistir və ya dəyişdir', '<modul> <mesaj və ya cavab>', 'Dəyişdir əmri, botdakı plugin mesajlarını dəyişdirmənizə yarayır. Əgər mesaj yazmasanız Plugin mesajını orijinal vəziyyətinə qaytarar.'
).add_info(
    '**Dəyişəbilən Pluginlər:** `afk/alive/pm/kickme/dızcı/ban/mute/approve/disapprove/block`\n**Alive Dəyişənləri:** `{plugin}, {telethon}, {brend}, {python}`\n\
**Ban/Mute Dəyişənləri:** `{id}, {username}, {first_name}, {last_name}, {mention}, {date}, {count}`\n\
**AFK Dəyişənləri:** `{username}, {mention}, {first_name}, {last_name}, {last_seen_seconds}, {last_seen}, {last_seen_long}`\n\
**PMpermit Dəyişkənləri(pm, block, approve, disapprove):** `{id}, {username}, {mention}, {first_name}, {last_name}`\n\
**Kickme Dəyişəni:** `{istədiyiniz mətn}`'
).add()
