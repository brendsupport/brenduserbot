from userbot.events import register
from userbot import CMD_HELP, BOTLOG_CHATID
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value
LANG = get_value("snips")


@register(outgoing=True, pattern=r"\$\w*", ignore_unsafe=True, disable_errors=True)
async def on_snip(event):
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if snip and snip.f_mesg_id:
        await event.delete()
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID, ids=int(snip.f_mesg_id))
        await event.client.send_message(event.chat_id, msg_o.message, reply_to=message_id_to_reply, file=msg_o.media)
    elif snip and snip.reply:
        await event.client.send_message(event.chat_id, snip.reply, reply_to=message_id_to_reply)


@register(outgoing=True, pattern="^.snip (\w*)")
async def on_snip_save(event):
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AtrributeError:
        await event.edit(LANG['NO_SQL'])
        return
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(BOTLOG_CHATID, f"#SNIP\n🔑 Açar söz: {keyword}\n⬇️ Aşağıdakı mesaj snip olaraq yaddaşda saxlanır!")
            msg_o = await event.client.forward_messages(BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(LANG['NEED_BOTLOG'])
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`💾 Snip {}. {}:` **${}** `"
    if add_snip(keyword, string, msg_id) is False:
        await event.edit(success.format(LANG['UPDATED'], LANG['USAGE'], keyword))
    else:
        await event.edit(success.format(LANG['SAVED'], LANG['USAGE'], keyword))


@register(outgoing=True, pattern="^.snips$")
async def on_snip_list(event):
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        await event.edit("`SQL dan kənar modda işləyir!`")
        return
    message = LANG['NO_SNIP']
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == LANG['NO_SNIP']:
            message = f"{LANG['SNIPS']}:\n"
            message += f"`${a_snip.snip}`\n"
        else:
            message += f"`${a_snip.snip}`\n"
    await event.edit(message)


@register(outgoing=True, pattern="^.remsnip (\w*)")
async def snip_delete(event):
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        await event.edit("`SQL dan kənar modda işləyir!`")
        return
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"`Snip:` **{name}** `{LANG['DELETED']}`")
    else:
        await event.edit(f"`Snip:` **{name}** `{LANG['NOT_FOUND']}` ")

CmdHelp('snips').add_command(
    '$<snip_adı>', None, 'Snipi çağırar.'
).add_command(
    'snip', '<ad> <məlumat/cavab>', 'Bir snip olaraq qeyd edər. (Şəkil,səs və stickerlərlə işləyər !)'
).add_command(
    'snips', None, 'Yülkənən bütün snip\'ləri atar.'
).add_command(
    'remsnip', '<snip adı>', 'Qeyd olunan snip\'i silər.'
).add()
