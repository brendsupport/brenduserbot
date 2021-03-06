from userbot.events import register
from userbot import CMD_HELP, bot, LOGS, CLEAN_WELCOME, BOTLOG_CHATID
from telethon.events import ChatAction
from userbot.cmdhelp import CmdHelp

@bot.on(ChatAction)
async def welcome_to_chat(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
        from userbot.modules.sql_helper.welcome_sql import update_previous_welcome
    except:
        return
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        """user_added=True,
        user_joined=True,
        user_left=False,
        user_kicked=False"""
        if (event.user_joined
                or event.user_added) and not (await event.get_user()).bot:
            if CLEAN_WELCOME:
                try:
                    await event.client.delete_messages(event.chat_id,
                                                       cws.previous_welcome)
                except Exception as e:
                    LOGS.warn(str(e))
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            mention = "[{}](tg://user?id={})".format(a_user.first_name,
                                                     a_user.id)
            my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            my_first = me.first_name
            my_last = me.last_name
            if my_last:
                my_fullname = f"{my_first} {my_last}"
            else:
                my_fullname = my_first
            my_username = f"@{me.username}" if me.username else my_mention
            file_media = None
            current_saved_welcome_message = None
            if cws and cws.f_mesg_id:
                msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(cws.f_mesg_id))
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
            elif cws and cws.reply:
                current_saved_welcome_message = cws.reply
            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention,
                                                     title=title,
                                                     count=count,
                                                     first=first,
                                                     last=last,
                                                     fullname=fullname,
                                                     username=username,
                                                     userid=userid,
                                                     my_first=my_first,
                                                     my_last=my_last,
                                                     my_fullname=my_fullname,
                                                     my_username=my_username,
                                                     my_mention=my_mention),
                file=file_media)
            update_previous_welcome(event.chat_id, current_message.id)


@register(outgoing=True, pattern=r"^.setwelcome(?: |$)(.*)")
async def save_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import add_welcome_setting
    except:
        await event.edit("`SQL dan k??nar modda i??l??yir!`")
        return
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#QAR??ILAMA_QEYD??\
            \nQRUP ID: {event.chat_id}\
            \nA??a????dak?? mesaj s??hb??t ??????n yeni Qar????lama qeydi olarak qeyd edildi, xai?? edirik silm??yin !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Qar????lama  notunu yadda saxlamaq ??????n BOTLOG_CHATID t??nziml??nm??si laz??md??r.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Bu s??hb??t ??????n qar????lama mesaj?? {} `"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format('qeyd edildi'))
    else:
        await event.edit(success.format('g??nc??ll??ndi'))


@register(outgoing=True, pattern="^.checkwelcome$")
async def show_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
    except:
        await event.edit("`SQL rejimind??n k??narda i??l??yir!`")
        return
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        await event.edit("`Burada qar????lama mesaj?? saxlan??lmay??b.`")
        return
    elif cws and cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(cws.f_mesg_id))
        await event.edit(
            "`Hal-haz??rda bu qar????lama qeydi il?? yeni istifad????il??ri qar????lay??ram.`")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws and cws.reply:
        await event.edit(
            "`Hal-haz??rda bu qar????lama qeydi il?? yeni istifad????il??ri qar????lay??ram.`")
        await event.reply(cws.reply)


@register(outgoing=True, pattern="^.rmwelcome$")
async def del_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import rm_welcome_setting
    except:
        await event.edit("`SQL rejimind??n k??narda i??l??yir!`")
        return
    if rm_welcome_setting(event.chat_id) is True:
        await event.edit("`Xo?? g??ldiniz mesaj?? bu s??hb??t ??????n silindi.`")
    else:
        await event.edit("`Burada qar????lama qeydi varm???`")


CMD_HELP.update({
    "welcome":
    "\
.setwelcome <qar????lama mesaj??> v?? ya .setwelcome il?? bir mesaja cavab verin\
\n??stifad??: Mesaj?? s??hb??t ??????n qar????lama qeydi kimi saxlay??r.\
\n\nQar????lama mesaj??n?? formatla??d??rmaq ??????n m??vcud d??yi????nl??r :\
\n`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`\
\n\n.checkwelcome\
\n??stifad??: S??hb??td?? qar????lama qeydi olub olmad??????n?? yoxlay??r.\
\n\n.rmwelcome\
\nKullan??m: Se??ili bir s??hb??t ??????n xo?? g??ldiniz qeydini sil??r.\
"
})

CmdHelp('welcome').add_command(
    'setwelcome', '<qar????lama mesaj??>', 'Mesaj?? sohbet ??????n qar????lama qeydi kimi saxlay??r.'
).add_command(
    'checkwelcome', None, 'S??hbwtdw qar????lama qeydi olub olmad??????n?? yoxlay??r.'
).add_command(
    'rmwelcome', None, 'Cari s??hb??t ??????n xo?? g??ldiniz qeydini silir.'
).add_info(
    'D??yi????nl??r: `{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`'
).add()
