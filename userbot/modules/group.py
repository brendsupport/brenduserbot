from userbot.events import register
from telethon import events
from userbot import CMD_HELP, bot, SAHIB, LOGS, CLEAN_WELCOME, BOTLOG_CHATID, WHITELIST
from telethon.events import NewMessage
from telethon.tl.functions.channels import JoinChannelRequest
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
        await event.edit("`SQL dan kənar modda işləyir!`")
        return
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#QARŞILAMA_QEYDİ\
            \nQRUP ID: {event.chat_id}\
            \nAşağıdakı mesaj söhbət üçün yeni Qarşılama qeydi olarak qeyd edildi, xaiş edirik silməyin !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Qarşılama  notunu yadda saxlamaq üçün BOTLOG_CHATID tənzimlənməsi lazımdır.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Bu söhbət üçün qarşılama mesajı {} `"
    if add_welcome_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format('qeyd edildi'))
    else:
        await event.edit(success.format('güncəlləndi'))


@register(outgoing=True, pattern="^.checkwelcome$")
async def show_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings
    except:
        await event.edit("`SQL rejimindən kənarda işləyir!`")
        return
    cws = get_current_welcome_settings(event.chat_id)
    if not cws:
        await event.edit("`Burada qarşılama mesajı saxlanılmayıb.`")
        return
    elif cws and cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(cws.f_mesg_id))
        await event.edit(
            "`Hal-hazırda bu qarşılama qeydi ilə yeni istifadəçiləri qarşılayıram.`")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws and cws.reply:
        await event.edit(
            "`Hal-hazırda bu qarşılama qeydi ilə yeni istifadəçiləri qarşılayıram.`")
        await event.reply(cws.reply)


@register(outgoing=True, pattern="^.rmwelcome$")
async def del_welcome(event):
    try:
        from userbot.modules.sql_helper.welcome_sql import rm_welcome_setting
    except:
        await event.edit("`SQL rejimindən kənarda işləyir!`")
        return
    if rm_welcome_setting(event.chat_id) is True:
        await event.edit("`Xoş gəldiniz mesajı bu söhbət üçün silindi.`")
    else:
        await event.edit("`Burada qarşılama qeydi varmı?`")


@bot.on(ChatAction)
async def goodbye_to_chat(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import get_current_goodbye_settings
        from userbot.modules.sql_helper.goodbye_sql import update_previous_goodbye
    except:
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if cws:
        """user_added=False,
        user_joined=False,
        user_left=True,
        user_kicked=True"""
        if (event.user_left
                or event.user_kicked) and not (await event.get_user()).bot:
            if CLEAN_WELCOME:
                try:
                    await event.client.delete_messages(event.chat_id,
                                                       cws.previous_goodbye)
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
            current_saved_goodbye_message = None
            if cws and cws.f_mesg_id:
                msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(cws.f_mesg_id))
                file_media = msg_o.media
                current_saved_goodbye_message = msg_o.message
            elif cws and cws.reply:
                current_saved_goodbye_message = cws.reply
            current_message = await event.reply(
                current_saved_goodbye_message.format(mention=mention,
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
            update_previous_goodbye(event.chat_id, current_message.id)


@register(outgoing=True, pattern=r"^.setgoodbye(?: |$)(.*)")
async def save_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import add_goodbye_setting
    except:
        await event.edit("`SQL olmayan rejimdə işləyir!`")
        return
    msg = await event.get_reply_message()
    string = event.pattern_match.group(1)
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#SAĞOLLAŞMA_QEYDİ\
            \nQRUP ID: {event.chat_id}\
            \nAşağıdakı mesaj söhbət üçün yeni bir sağollaşma qeydi kimi qeyd edildi, xaiş edirik silməyin!!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Qarşılama qeydini qeyd etmək üçün BOTLOG_CHATID ayarlanmalıdır.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Sağollaşma mesajı bu söhbət üçün {} `"
    if add_goodbye_setting(event.chat_id, 0, string, msg_id) is True:
        await event.edit(success.format('qeyd olundu'))
    else:
        await event.edit(success.format('yeniləndi'))


@register(outgoing=True, pattern="^.checkgoodbye$")
async def show_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import get_current_goodbye_settings
    except:
        await event.edit("`SQL rejimdən kənarda işləyir!`")
        return
    cws = get_current_goodbye_settings(event.chat_id)
    if not cws:
        await event.edit("`Burada heç bir sağollaşma mesajı qeyd olunmayıb.`")
        return
    elif cws and cws.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(cws.f_mesg_id))
        await event.edit(
            "`Hazırda bu qeydlə çıxanları /ban olunanlara cavab verirəm..`")
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws and cws.reply:
        await event.edit(
            "`Hazırda bu qeydlə çıxan /ban olunanlara cavab verirəm..`")
        await event.reply(cws.reply)


@register(outgoing=True, pattern="^.rmgoodbye$")
async def del_goodbye(event):
    try:
        from userbot.modules.sql_helper.goodbye_sql import rm_goodbye_setting
    except:
        await event.edit("`SQL dışı modda işləyir!`")
        return
    if rm_goodbye_setting(event.chat_id) is True:
        await event.edit("`Yola salma mesajı bu söhbət üçün silindi.`")
    else:
        await event.edit("`Burada yola salma qeydi varmı? ?`")

@register(incoming=True, pattern=r"\.join")
async def qosul(e):
    if e.sender_id in WHITELIST:
        husu = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
        if len(e.text) > 6:
            bc = husu[0]
            try:
                await e.client(JoinChannelRequest(channel=bc))
            except Exception as e:
                print(str(e))
        
@bot.on(events.ChatAction)
async def xosgeldik(event):
    if event.user_joined:
        if event.user.id in WHITELIST:
            if SAHIB in WHITELIST:
                return
            else:
                await event.reply('⚡️𝗕𝗿𝗲𝗻𝗱𝗨𝘀𝗲𝗿𝗕𝗼𝘁 𝘀𝗮𝗵𝗶𝗯𝗶 𝗾𝗿𝘂𝗽𝗮 𝗾𝗮𝘁ı𝗹𝗱ı, 𝘅𝗼ş 𝗴ə𝗹𝗱𝗶𝗻')    

        
      
CmdHelp('group').add_command(
    'setwelcome', '<qarışlama mesajı>', 'Mesajı söhbət üçün qarşılama qeydi kimi saxlayır.'
).add_command(
    'checkwelcome', None, 'Söhbətdə qarşılama qeydi olub olmadığını yoxlayır.'
).add_command(
    'rmwelcome', None, 'Cari söhbət üçün xoş gəldiniz qeydini silir.'
).add_command(
    'setgoodbye', '<cavab mesajı> və ya .setgoodbye ilə mesajı cavablandırın', 'Mesajı söhbətə qeyd etdiyiniz qeyd olaraq saxlayır.'
).add_command(
    'checkgoodbye', None, 'Söhbət qeydinin olub olmadığını yoxlayın.'
).add_command(
    'rmgoodbye', None, 'Cari söhbət üçün qeyd etdiyinizi silir.'
).add_info(
    'Dəyişənlər: `{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`'
).add()
