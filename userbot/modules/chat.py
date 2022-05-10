from asyncio import sleep
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors import rpcbaseerrors
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, bot, SAHIB, DEFAULT_NAME
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot.main import PLUGIN_MESAJLAR
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value
LANG = get_value("chat")

@register(outgoing=True, pattern=r"^.lock ?(.*)")
async def locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = True
        what = "messages"
    elif input_str == "media":
        media = True
        what = "media"
    elif input_str == "sticker":
        sticker = True
        what = "stickers"
    elif input_str == "gif":
        gif = True
        what = "GIFs"
    elif input_str == "game":
        gamee = True
        what = "games"
    elif input_str == "inline":
        ainline = True
        what = "inline bots"
    elif input_str == "poll":
        gpoll = True
        what = "polls"
    elif input_str == "invite":
        adduser = True
        what = "invites"
    elif input_str == "pin":
        cpin = True
        what = "pins"
    elif input_str == "info":
        changeinfo = True
        what = "chat info"
    elif input_str == "all":
        msg = True
        media = True
        sticker = True
        gif = True
        gamee = True
        ainline = True
        gpoll = True
        adduser = True
        cpin = True
        changeinfo = True
        what = "everything"
    else:
        if not input_str:
            await event.edit(LANG['EVERYTHING_LOCK'])
            return
        else:
            await event.edit(LANG['INVALID_MEDIA_TYPE'] % input_str)
            return

    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(peer=peer_id,
                                               banned_rights=lock_rights))
        await event.edit(LANG['LOCK'] % what)
    except BaseException as e:
        await event.edit(
            f"{LANG['INVALID_AUTHORITY']} {str(e)}")
        return


@register(outgoing=True, pattern=r"^.unlock ?(.*)")
async def rem_locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = False
        what = "messages"
    elif input_str == "media":
        media = False
        what = "media"
    elif input_str == "sticker":
        sticker = False
        what = "stickers"
    elif input_str == "gif":
        gif = False
        what = "GIFs"
    elif input_str == "game":
        gamee = False
        what = "games"
    elif input_str == "inline":
        ainline = False
        what = "inline bots"
    elif input_str == "poll":
        gpoll = False
        what = "polls"
    elif input_str == "invite":
        adduser = False
        what = "invites"
    elif input_str == "pin":
        cpin = False
        what = "pins"
    elif input_str == "info":
        changeinfo = False
        what = "chat info"
    elif input_str == "all":
        msg = False
        media = False
        sticker = False
        gif = False
        gamee = False
        ainline = False
        gpoll = False
        adduser = False
        cpin = False
        changeinfo = False
        what = "everything"
    else:
        if not input_str:
            await event.edit(LANG['EVERYTHING_UNLOCK'])
            return
        else:
            await event.edit(LANG['INVALID_MEDIA_TYPE'] % input_str)
            return

    unlock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(peer=peer_id,
                                               banned_rights=unlock_rights))
        await event.edit(LANG['UNLOCK'] % what)
    except BaseException as e:
        await event.edit(
            f"{LANG['INVALID_AUTHORITY']} {str(e)}")
        return

@register(outgoing=True, pattern="^.id")
async def chatid(e):
    message = await e.get_reply_message()
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
        await e.edit(f"{LANG['NAME']} **{message.sender.first_name}\n{LANG['USERNAME']} {name}\n{LANG['ID']}** `{user_id}`")
    else: 
        await e.edit(f"{LANG['NAME']} **{DEFAULT_NAME}\n{LANG['ID']}** {SAHIB}\n{LANG['GROUP']} `{e.chat_id}`")


@register(outgoing=True, pattern="^.link(?: |$)(.*)")
async def link(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        await mention.edit(f"[{custom}](tg://user?id={user.id})")
    else:
        tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
        await mention.edit(f"[{tag}](tg://user?id={user.id})")
        
        
@register(outgoing=True, pattern="^.temizle$")
async def fastpurger(purg):

    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit(LANG['NEED_MSG'])
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id, LANG['PURGED'].format(str(count)))

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "Hədəflənən " + str(count) + " mesaj müvəffəqiyyətlə silindi.")
    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern="^.purgeme")
async def purgeme(delme):
    
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id,
                                                    from_user='me'):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        LANG['PURGED_ME'].format(str(count))
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "Hədəflənən " + str(count) + " mesajınız müvəffəqiyyətlə silindi.")
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern="^.sil$")
async def delete_it(delme):

    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Hədəflənən mesajın silinməsi müvəffəqiyyətlə tamamlandı")
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Bu mesajı silə bilmirəm.")
        

@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    chat = await leave.get_chat()
    await leave.edit(f"{PLUGIN_MESAJLAR['kickme']}".format(
        id=chat.id,
        title=chat.title,
        member_count="Bilinmir" if chat.participants_count == None else (chat.participants_count - 1)
    ))
    await leave.client.kick_participant(leave.chat_id, 'me')

CmdHelp('chat').add_command(
    'id', None, 'Cavab verərək yazsanız həmin istifadəçinin, Boş yazsanız sizin ID məlumatlarınızı verəcək'
).add_command(
    'link', '<cavab>', 'Cavab verdiyiniz istifadəçiyə anlıq adlı link qoya bilərsiniz'
).add_command(
    'kickme', None, 'Qrupdan ayrılarsınız'
).add_command(
    'temizle', None, 'Hədəflenen mesajdan başlayaraq sona qədər olan bütün mesajları silər.'
).add_command(
    'purgeme', 'Hədəflənən mesajdan başlayaraq öz mesajlarınızı silər.'
).add_command(
    'sil', '<cavab>', 'Göstərdiyiniz mesajı silir.'
).add_command(
    'lock', '<kilidləmək üçün media növü> və ya .unlock <kilid açmaq üçün media növü>', 'Söhbət gifindəki bəzi xüsusiyyətləri birləşdirin, media, stiker və s kimi'
).add_info(
    'Kilidləyə biləcəyiniz şeylər: all, msg, media, sticker, gif, game, inline, poll, invite, pin, info'
).add()
