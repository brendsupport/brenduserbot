from userbot.language import get_value
LANG = get_value("chat")

from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot.main import PLUGIN_MESAJLAR

@register(outgoing=True, pattern="^.id$")
async def useridgetter(target):

    message = await target.get_reply_message()
    if message:
        if not message.forward:
            user_id = message.sender.id
            if message.sender.username:
                name = "@" + message.sender.username
            else:
                name = "**" + message.sender.first_name + "**"
        else:
            user_id = message.forward.sender.id
            if message.forward.sender.username:
                name = "@" + message.forward.sender.username
            else:
                name = "*" + message.forward.sender.first_name + "*"
        await target.edit("**{}** {} \n**{}** `{}`".format(
            LANG['USERNAME'], name, LANG['ID'], user_id))


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def permalink(mention):

    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = user.first_name.replace("\u2060",
                                      "") if user.first_name else user.username
        await mention.edit(f"[{tag}](tg://user?id={user.id})")


@register(outgoing=True, pattern="^.qrupid$")
async def chatidgetter(chat):

    await chat.edit(f"{LANG['GROUP']} `" + str(chat.chat_id) + "`")


@register(outgoing=True, pattern=r"^.log(?: |$)([\s\S]*)")
async def log(log_text):

    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Grup ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`Bununla nə etməliyəm?`")
            return
        await log_text.edit("`Günlüyə qeyd olundu`")
    else:
        await log_text.edit(LANG['NEED_LOG'])
    await sleep(2)
    await log_text.delete()


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):

    chat = await leave.get_chat()
    await leave.edit(f"{PLUGIN_MESAJLAR['kickme']}".format(
        id=chat.id,
        title=chat.title,
        member_count="Bilinmir" if chat.participants_count == None else (chat.participants_count - 1)
    ))
    await leave.client.kick_participant(leave.chat_id, 'me')


@register(outgoing=True, pattern="^.unmuteqrup$")
async def unmute_chat(unm_e):

    try:
        from userbot.modules.sql_helper.keep_read_sql import unkread
    except AttributeError:
        await unm_e.edit('`SQL rejimindən kənarda işləyir!`')
        return
    unkread(str(unm_e.chat_id))
    await unm_e.edit(LANG['UNMUTED'])
    await sleep(2)
    await unm_e.delete()


@register(outgoing=True, pattern="^.muteqrup$")
async def mute_chat(mute_e):

    try:
        from userbot.modules.sql_helper.keep_read_sql import kread
    except AttributeError:
        await mute_e.edit("`SQL rejimindən kənarda işləyir!`")
        return
    await mute_e.edit(str(mute_e.chat_id))
    kread(str(mute_e.chat_id))
    await mute_e.edit(LANG['MUTED'])
    await sleep(2)
    await mute_e.delete()
    if BOTLOG:
        await mute_e.client.send_message(
            BOTLOG_CHATID,
            str(mute_e.chat_id) + " susduruldu.")


@register(incoming=True, disable_errors=True)
async def keep_read(message):

    try:
        from userbot.modules.sql_helper.keep_read_sql import is_kread
    except AttributeError:
        return
    kread = is_kread()
    if kread:
        for i in kread:
            if i.groupid == str(message.chat_id):
                await message.client.send_read_acknowledge(message.chat_id)

regexNinja = False


@register(outgoing=True, pattern="^s/")
async def sedNinja(event):

    if regexNinja:
        await sleep(.5)
        await event.delete()


@register(outgoing=True, pattern="^.regexninja (on|off)$")
async def sedNinjaToggle(event):

    global regexNinja
    if event.pattern_match.group(1) == "on":
        regexNinja = True
        await event.edit("`Regexbot üçün ninja rejimi aktiv edildi.`")
        await sleep(1)
        await event.delete()
    elif event.pattern_match.group(1) == "off":
        regexNinja = False
        await event.edit("`Regexbot üçün ninja rejimi deaktiv edildi.`")
        await sleep(1)
        await event.delete()



CMD_HELP.update({
    "chat":
    ".chatid\
\nİstifadə: Göstərilən qrupun İD nömrəsini verir\
\n\n.userid\
\nİstifadə: Göstərilən istifadəçinin İD nömrəsini verir.\
\n\n.log\n\nİstifadə: Cavablanmış mesajı Gündəlik qrupuna göndərir.\
\n\n.kickme\
\nİstifadə: Göstərilən qrupdan çıxmağınıza imkan verir.\
\n\n.unmutechat\
\nİstifadə: Səssizdə olan qrupun səsini açar.\
\n\n.mutechat\
\nİstifadə: Göstərilən qrupu susdurur.\
\n\n.link <istifadəçi adı/İstifadəçi id> : <istəyə bağlı mətn> (və ya) kiminsə mesajına .link ilə cavab verərək <isteğe bağlı mətnn>\
\nİstifadə: İstəyə uyğun xüsusi mətn ilə istifadəçi profilinə qalıcı bir əlaqə yaradın.\
\n\n.regexninja on/off\
\nİstifadə: Regex ninja modulunu qlobal olaraq aktivləşdirir / qeyri aktiv edir.\
\nRegex ninja modulu, regex botunun yaratdığı mesajları silməyə kömək edir."
})
