import io
import re

import userbot.modules.sql_helper.blacklist_sql as sql
from userbot import CMD_HELP
from userbot.events import register
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("blacklist")

KUFURLER = ["amcıq","oğraş","qəhbə","erməni","amciq","göt","got","qehbe","sik","peyser","peysər","faise","amciq","osduraq","seks","götəş","gotes","sikis","sikim","peysər","faise","amciq","osduraq","seks","götəş","gotes","sikis","amck","anani","ananin","ananisikerim","anani sikerim","ananisikeyim","anani sikeyim","orospu","anasi"]
@register(incoming=True, disable_edited=True, disable_errors=True)
async def on_new_message(event):
    name = event.raw_text
    snips = sql.get_chat_blacklist(event.chat_id)
    for snip in snips:
        if snip == "söyüş":
            for kufur in KUFURLER:
                pattern = r"( |^|[^\w])" + re.escape(kufur) + r"( |$|[^\w])"
                if re.search(pattern, name, flags=re.IGNORECASE):
                    try:
                        await event.delete()
                    except:
                        await event.reply(LANG['FORBIDDEN_KUFUR'])
                        sql.rm_from_blacklist(event.chat_id, "soyus")
                    break
                pass
            continue
        else:
            pattern = r"( |^|[^\w])" + re.escape(snip) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                try:
                    await event.delete()
                except Exception as e:
                    await event.reply(LANG['HAVENT_PERMISSION'])
                    sql.rm_from_blacklist(event.chat_id, snip.lower())
                break
            pass



@register(outgoing=True, pattern="^.söyüş ?(.*)")
async def kufur(event):
    kufur = event.pattern_match.group(1)
    if len(kufur) < 1:
        await event.edit(LANG['USAGE_KUFUR'])
    
    if kufur == "aç":
        sql.add_to_blacklist(event.chat_id, "söyüş")
        await event.edit(LANG['OPENED_KUFUR'])
    elif kufur == "bağla":
        if sql.rm_from_blacklist(event.chat_id, "söyüş"):
            await event.edit(LANG['CLOSED_KUFUR'])
        else:
            await event.edit(LANG['ALREADY_CLOSED_KUFUR'])


@register(outgoing=True, pattern="^.addblacklist(?: |$)(.*)")
async def on_add_black_list(addbl):
    if addbl.is_reply:
        reply = await addbl.get_reply_message()
        text = reply.text
    else:
        text = addbl.pattern_match.group(1)
    to_blacklist = text.split()
    for trigger in to_blacklist:
        sql.add_to_blacklist(addbl.chat_id, trigger)
    await addbl.edit("{} **{}**".format(len(to_blacklist), LANG['ADDED']))

@register(outgoing=True, pattern="^.listblacklist(?: |$)(.*)")
async def on_view_blacklist(listbl):
    all_blacklisted = sql.get_chat_blacklist(listbl.chat_id)
    OUT_STR = f"**{LANG['BLACKLIST']}**\n"
    if len(all_blacklisted) > 0:
        for trigger in all_blacklisted:
            OUT_STR += f"`{trigger}`\n"
    else:
        OUT_STR = LANG['NOT_FOUND']
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "blacklist.text"
            await listbl.client.send_file(
                listbl.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=LANG['BLACKLIST_FILE'],
                reply_to=listbl
            )
            await listbl.delete()
    else:
        await listbl.edit(OUT_STR)

@register(outgoing=True, pattern="^.rmblacklist(?: |$)(.*)")
async def on_delete_blacklist(rmbl):
    text = rmbl.pattern_match.group(1)
    to_unblacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
    successful = 0
    for trigger in to_unblacklist:
        if sql.rm_from_blacklist(rmbl.chat_id, trigger.lower()):
            successful += 1
    await rmbl.edit(LANG['REMOVED'])
    
CmdHelp('blacklist').add_command(
    'listblacklist', None, 'Söhbətdəki aktiv qara siyahını siyahıya alır.'
).add_command(
    'addblacklist', '<söz(lər)/cavab>', 'Mesajı \'qara siyahının açar sözlərində\' saxlayar. \'Qara siyahının açar sözlərindən\' bəhs olunduqda, bot mesajı siləcəkdir.', '.addblacklist amk'
).add_command(
    'rmblacklist', '<söz>', 'Göstərilən qara siyahını dayandırır.', '.rmblacklist amk'
).add_warning('Bu əməliyyatları yerinə yetirmək üçün idarəçi olmalısınız **Mesaj Silmə** səlahiyyətiniz olmalıdır.').add()
