import os, asyncio, emoji
import threading
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from googletrans import LANGUAGES, Translator

from telethon.tl.types import ChatAdminRights
from telethon import events
from time import sleep
from youtube_search import YoutubeSearch
from userbot.events import register
from userbot import bot, CMD_HELP, BOTLOG, BOTLOG_CHATID
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value
LANG = get_value("tools")


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call, limit=1))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]



@register(outgoing=True, pattern=r"^\.bvc$", groups_only=True)
async def start_voice(brend):
    chat = await brend.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await brend.edit("`Admin deyilsiniz`")
        return
    try:
        await brend.client(startvc(brend.chat_id))
        await brend.edit("`Səsli söhbət uğurla başladıldı✔️`")
    except Exception as ex:
        await brend.edit(f"**ERROR:** `{ex}`")


@register(outgoing=True, pattern=r"^\.svc$", groups_only=True)
async def stop_voice(brend):
    chat = await brend.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await brend.edit("`Admin deyilsiniz..`")
        return
    try:
        await brend.client(stopvc(await get_call(brend)))
        await brend.edit("**Səsli söhbət sonlandırıldı✔️**")
    except Exception as ex:
        await brend.edit(f"**ERROR:** `{ex}`")


@register(outgoing=True, pattern=r"^\.dvc", groups_only=True)
async def _(brend):
    xxnx = await brend.edit("`Istifadəçilər səsli söhbətə dəvət edilir...`")
    users = []
    z = 0
    async for x in brend.client.iter_participants(brend.chat_id):
        if not x.bot:
            users.append(x.id)
    botman = list(user_list(users, 6))
    for p in botman:
        try:
            await brend.client(invitetovc(call=await get_call(brend), users=p))
            z += 6
        except BaseException:
            pass
    await xxnx.edit(f"`{z}` **istifadəçi dəvət olundu✔️**")

@register(outgoing=True, pattern=r"^\.advc(?: |$)(.*)", groups_only=True)
async def change_title(brend):
    title = brend.pattern_match.group(1)
    chat = await brend.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await brend.edit("`Zəhmət olmasa bir başlıq yazın..`")

    if not admin and not creator:
        await brend.edit("`Admin deyilsiniz..`")
        return
    try:
        await brend.client(settitle(call=await get_call(brend), title=title.strip()))
        await brend.edit(f"**Səsli söhbət başlığı uğurla dəyişdirildi✔️**\n\n**yeni başlıq :** `{title}`")
    except Exception as ex:
        await brend.edit(f"**ERROR:** `{ex}`")
  
@register(outgoing=True, pattern="^.sangmata(?: |$)(.*)")
async def sangmata(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit(LANG['REPLY_MSG'])
       return
    chat = "@SangMataInfo_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_BOT_ERROR'])
       return
    await event.edit(LANG['WORKING_ON'])
    async with bot.conversation(chat, exclusive=False) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit(LANG['BLOCKED_ERROR'])
              return
          except Exception as e:
              print(e.__class__)
          if not response:
              await event.edit(LANG['NOT_RESPONSE'])
          elif response.text.startswith("Forward"):
             await event.edit(LANG['USER_PRIVACY'])
          else: 
             await event.edit(response.text)
          sleep(1)
          await bot.send_read_acknowledge(chat, max_id=(response.id+3))
          await conv.cancel_all()


@register(outgoing=True, pattern="^.arsiv")
async def creation(event):
    if not event.reply_to_msg_id:
        await event.edit(LANG['REPLY_TO_MSG'])
        return
    reply_message = await event.get_reply_message() 
    if event.fwd_from:
        return 
    chat = "@creationdatebot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['CALCULATING_TIME'])
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Hmm düşünürəmki` {chat} `əngəllənmisən. Xaiş edirik əngəli aç.`")
            return
        response = conv.wait_event(events.NewMessage(incoming=True,from_users=747653812))
        response = await response
        if response.text.startswith("Looks"):
            await event.edit(LANG['PRIVACY_ERR'])
        else:
            await event.edit(f"**Hesabat hazır: **`{response.text.replace('**','')}`")


@register(outgoing=True, pattern="^.read")
async def brendread(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@bacakubot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['READING'])
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Hmm düşünürəmki` {chat} `əngəllənmisən. Xaiş edirik əngəli aç.`")
            return
        response = conv.wait_event(events.NewMessage(incoming=True,from_users=834289439))
        response = await response
        if response.text.startswith("Please try my other cool bot:"):
            response = conv.wait_event(events.NewMessage(incoming=True,from_users=834289439))
            response = await response
        if response.text == "":
            await event.edit(LANG['OCR_ERROR'])
        else:
            await event.edit(f"**{LANG['SEE_SOMETHING']}: **`{response.text}`")

@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def quotly(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['QUOTING'])
    async with bot.conversation(chat, exclusive=False, replies_are_responses=True) as conv:
        response = None
        try:
            sayi = event.pattern_match.group(1)
            if len(sayi) == 1:
                sayi = int(sayi)
                i = 1
                mesajlar = [event.reply_to_msg_id]
                while i < sayi:
                    mesajlar.append(event.reply_to_msg_id + i)
                    i += 1
                msg = await event.client.forward_messages(chat, mesajlar, from_peer=event.chat_id)
            else:
                msg = await reply_message.forward_to(chat)
            response = await conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739), timeout=10)
        except YouBlockedUserError: 
            await event.edit(LANG['UNBLOCK_QUOTLY'])
            return
        except asyncio.TimeoutError:
            await event.edit("`Botdan cavab ala bilmədim!`")
            return
        except ValueError:
            await event.edit(LANG['QUOTLY_VALUE_ERR'])
            return
        if not response:
            await event.edit("`Botdan cavab ala bilmədim!`")
        elif response.text.startswith("Salam ALeykum!"):
            await event.edit(LANG['USER_PRIVACY'])
        else: 
            await event.delete()
            await response.forward_to(event.chat_id)
        await conv.mark_read()
        await conv.cancel_all()


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(event):
    if event.fwd_from:
        return
    ttss = event.pattern_match.group(1)
    rep_msg = None
    if event.is_reply:
        rep_msg = await event.get_reply_message()
    if len(ttss) < 1:
        if event.is_reply:
            sarki = rep_msg.text
        else:
            await event.edit("`Səsə çevirməyim üçün əmrin yanında bir mesaj yazmalısan.`")
            return
    await event.edit(f"__Mesajınız səsə çevrilir...__")
    chat = "@MrTTSbot"
    async with bot.conversation(chat) as conv:
        try:     
            await conv.send_message(f"/tomp3 {ttss}")
        except YouBlockedUserError:
            await event.reply(f"{chat} əngəlləmisən. Xaiş olunur qadağanı aç.`")
            return
        ses = await conv.wait_event(events.NewMessage(incoming=True,from_users=1678833172))
        await event.client.send_read_acknowledge(conv.chat_id)
        indir = await ses.download_media()
        voice = await asyncio.create_subprocess_shell(f"ffmpeg -i '{indir}' -c:a libopus 'MrTTSbot.ogg'")
        await voice.communicate()
        if os.path.isfile("MrTTSbot.ogg"):
            await event.client.send_file(event.chat_id, file="MrTTSbot.ogg", voice_note=True, reply_to=rep_msg)
            await event.delete()
            os.remove("MrTTSbot.ogg")
        else:
            await event.edit("`Bir xəta yanadı!`")

            
@register(outgoing=True, pattern=r"^\.trt(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "az"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        return await event.edit("**.trt <dil kodu>** mesajlara cavab verərək")
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = """**🗣️ Tərcümə**\n`{}` dilindən - `{}` dilinə
\n📄 Mətn: `{}`""".format(
            translated.src, lan, after_tr_text
        )
        await event.edit(output_str)
    except Exception as exc:
        await event.edit(str(exc))


@register(outgoing=True, pattern="^.yt (.*)")
async def _(event):
    if event.fwd_from:
        return
    husu = event.pattern_match.group(1)
    editle = await event.edit("`Proses başladılır...`")
    results = YoutubeSearch(f"{husu}", max_results=5).to_dict()
    yazi = "<b>💻 YOUTUBE Axtarışı</b> \n\n"
    for ad in results:
      yazi += (
        f"<b><u>Başlıq</u></b> ➠ <code>{ad['title']}</code> \n"
        f"<b><u>Kanal</u></b> ➠ <code>{ad['channel']}</code> \n"
        f"<b><u>Müddət</u></b> ➠ <code>{ad['duration']}</code> \n"
        f"<b><u>Baxış</u></b> ➠ <code>{ad['views']}</code> \n"
        f"<b><u>Link</u></b> ➠  `https://www.youtube.com/watch?v={ad['id']}`\n\n"
        )
      await editle.edit(yazi, parse_mode="HTML")
        

@register(outgoing=True, pattern="^.tspam")
async def tmeme(e):
    message = e.text
    messageSplit = message.split(" ", 1)
    tspam = str(messageSplit[1])
    message = tspam.replace(" ", "")
    for letter in message:
        await e.respond(letter)
    await e.delete()
    if BOTLOG:
            await e.client.send_message(BOTLOG_CHATID, "#TSPAM \n\nTSpam uğurla edildi")

@register(outgoing=True, pattern="^.spam")
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        messageSplit = message.split(" ", 2)
        counter = int(messageSplit[1])
        spam_message = str(messageSplit[2])
        await asyncio.wait([e.respond(spam_message) for i in range(counter)])
        await e.delete()
        if BOTLOG:
            await e.client.send_message(BOTLOG_CHATID, "#SPAM \n\nSpam müvəffəqiyyətlə tamamlandı")

@register(outgoing=True, pattern="^.bigspam")
async def bigspam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        messageSplit = message.split(" ", 2)
        counter = int(messageSplit[1])
        spam_message = str(messageSplit[2])
        for i in range(1, counter):
            await e.respond(spam_message)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(BOTLOG_CHATID, "#BIGSPAM \n\nBigspam uğurla edildi")


@register(outgoing=True, pattern="^.delayspam")
async def delayspammer(e):
    # Teşekkürler @ReversedPosix
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        messageSplit= message.split(" ", 3)
        spam_delay = float(messageSplit[1])
        counter = int(messageSplit[2])
        spam_message = str(messageSplit[3])
        from userbot.events import register
        await e.delete()
        delaySpamEvent = threading.Event()
        for i in range(1, counter):
            await e.respond(spam_message)
            delaySpamEvent.wait(spam_delay)
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#DelaySPAM \n\n"
                "DelaySpam uğurla edildi"
                )

CmdHelp('tools').add_command(
    'img', '<söz>', 'Googleda sürətli bir fotoşəkil axtarır'
).add_command(
    'carbon', '<söz> və ya <cavab>', 'Carbon mətnini şəkilli halda göndərər.'
).add_command(
    'tts', '<söz>', 'Sözü səsə çevirin.'
).add_command(
    'trt', '<cavab>', 'Asand tərcümə modulu.'
).add_command(
    'yt', '<sorğu>', 'Youtube üzərində axtarış edər.'
).add_command(
    'sangmata', '<cavab>', 'Göstərdiyiniz istifadəçinin ad keçmişini göstərər'
).add_command(
    'q', '<say>', 'Mətni stikerə çevirin.'
).add_command(
    'read', '<cavab>', 'Şəkildəki yazını oxuyun.'
).add_command(
    'arsiv', '<cavab>', 'Cavab verdiyiniz istifadəçinin hesabı yaratma tarxini öyrənin.'
).add_command(
    'trt', '<söz>', 'Asand tərcümə modulu.'
).add_command(
    'bvc', '', 'Səsli söhbət başladar.'
).add_command(
    'svc', '', 'Səsli söhbəti sonlandırar.'
).add_command(
    'tspam', '<mətn>', 'Verdiyiniz mətnin hərflərini tək tək atar.'
).add_command(
    'spam', '<miqdar> <mətn>', 'Verilən miqdarda spam göndərər.'
).add_command(
    'bigspam', '<miqdar> <mətn>', 'Verilen miqdarda spam göndərər.'
).add_command(
    'delayspam', '<gecikme> <miktar> <metin>', 'Biraz gecikmə ilə spam atar.'
).add()
