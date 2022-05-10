# Bu moduldan nəsə oğurlayan peysərdi
# Brend Userbot

import os, asyncio
from userbot.events import register
from userbot import bot, CMD_HELP
from userbot.cmdhelp import CmdHelp
import asyncio
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterMusic, InputMessagesFilterVideo, InputMessagesFilterRoundVideo, InputMessagesFilterDocument, InputMessagesFilterUrl, InputMessagesFilterGif, InputMessagesFilterGeo, InputMessagesFilterContacts


@register(outgoing=True, pattern="^.status$")
async def fk(m):
    hs = await m.edit("Database -ə bağlanılır...")
    ms = str((await bot.get_messages(m.chat_id, limit=0)).total)
    ph = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterPhotos())).total)
    vi = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterVideo())).total)
    mu = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterMusic())).total)
    au = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterVideo())).total)
    vv = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterRoundVideo())).total)
    do = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterDocument())).total)
    urls = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterUrl())).total)
    gifs = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterGif())).total)
    geos = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterGeo())).total)
    cont = str((await bot.get_messages(m.chat_id, limit=0, filter=InputMessagesFilterContacts())).total)
    await asyncio.sleep(1)
    await hs.edit(f"✉️ Ümumi Mesaj: {ms}\n🖼 Ümumi Foto: {ph}\n📹 Ümumi Video Mesaj: {vi}\n🎵 Ümumi Musiqi Mesajı: {mu}\n🎶 Ümumi Audio: {au}\n🎥 Ümumi Video: {vv}\n📂 Ümumi Fayl: {do}\n🔗 Ümumi Link: {urls}\n🎞 Ümumi GIF: {gifs}\n🗺 Ümumi Məkan: {geos}\n👭 Ümumi Kontaktlar: {cont}")

@register(outgoing=True, pattern="^.qy (.*)")
async def b(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("Xahiş edirəm bir mətn verin")
    tt = event.text
    msg = tt[4:]
    kk = await event.edit("Mesajınız bütün qruplarınıza göndərilir 📢")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**Yayım yekunlaşdı📢**\nUğurlu {done} qrup✅ \n  Uğursuz {er} qrup❌")


@register(outgoing=True, pattern=r"^\.sy(?: |$)(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if not xx:
        return await event.edit("Xahiş edirəm bir mətn verin")
    tt = event.text
    msg = tt[4:]
    kk = await event.edit("Mesajınız bütün əlaqələrinizə göndərilir 📢")
    er = 0
    done = 0
    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
    await kk.edit(f"**Yayım yekunlaşdı📢**\nUğurlu {done} söhbət✅ \n  Uğursuz {er} söhbət❌")


@register(outgoing=True, pattern="^.unvoice(?: |$)(.*)")
async def mahnidanmesaja(event):
    caption = "@BrendUserBot ilə səsli mesaja çevirildi."
    if event.fwd_from:
        return
    mahni = event.pattern_match.group(1)
    rep_msg = None
    if event.is_reply:
        rep_msg = await event.get_reply_message()
    if len(sarki) < 1:
        if event.is_reply:
            mahni = rep_msg.text
        else:
            await event.edit("**Bir musiqiyə cavab ver!**") 
            return
    if event.is_reply:
        rep_msg = await event.get_reply_message()
        if rep_msg.audio:
            await event.edit(f"__Səs yüklənir...__")
            yukle = await rep_msg.download_media()
            await event.edit(f"__Səsi yüklədim, səsli mesaj olaraq göndərirəm...__")
            voice = await asyncio.create_subprocess_shell(f"ffmpeg -i '{yukle}' -y -c:a libopus 'brenevoice.ogg'")
            await voice.communicate()
            if os.path.isfile("brendvoice.ogg"):
                await event.client.send_file(event.chat_id, file="brendvoice.ogg", voice_note=True, caption=caption, reply_to=rep_msg)
                await event.delete()
                os.remove("brendvoice.ogg")
            else:
                await event.edit("Musiqini səsli mesaja çevirə bilmədim!")
            os.remove(yukle)
            return

@register(outgoing=True, pattern="^.gsend ?(.*)")
async def elcjn(brend):
    p = brend.pattern_match.group(1)
    m = p.split(" ")
    chat_id = m[0]
    try:
        chat_id = int(chat_id)
    except BaseException:
        pass
    msg = ""
    mssg = await brend.get_reply_message()
    if brend.reply_to_msg_id:
        await brend.client.send_message(chat_id, mssg)
        await brend.edit("`Mesaj göstərilən qrupa uğurla göndərildi✅`")
    for i in m[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await brend.client.send_message(chat_id, msg)
        await brend.edit("✅ Mesaj göstərilən qrupa uğurla göndərildi.")
    except BaseException:
        await brend.edit("**❌ Mesaj göndərilə bilmədi**")

@register(outgoing=True, pattern="^.oxu")
async def oxu(event):
    await event.delete()
    b = await event.client.download_media(await event.get_reply_message())
    a = open(b, "r")
    c = a.read()
    a.close()
    a = await event.reply("📝Fayl Oxunur...")
    if len(c) > 4096:
        await a.edit("🤦🏻‍♂️ Bu fayldakı ümumi söz sayı Teleqram limitindən çoxdur.")
    else:
        await a.edit(f"{c}")
    os.remove(b)

@register(outgoing=True, pattern="^.fayl ?(.*)")
async def fayl(event):
    await event.delete()
    a = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    b = open(input_str, "w")
    b.write(str(a.message))
    b.close()
    caption = f"[⚡ Brend Userbot](t.me/BrendUserbot) vasitəsilə yaradıldı."
    a = await event.reply(f"⏳ {input_str} faylı hazırlanır")
    await asyncio.sleep(1)
    await a.edit(f"📥 {input_str} faylı gətirilir")
    await asyncio.sleep(1)
    await event.client.send_file(event.chat_id, input_str, thumb = "userbot/modules/sql_helper/resources/Brend_Logo.jpg", caption = caption)
    await a.delete()
    os.remove(input_str)


CmdHelp('brend').add_command(
    'qy', '<mətn>', 'Verdiyiniz mətn olduğunuz bütün qruplara atılar'
).add_command(
    'sy', '<mətn>', 'Verdiyiniz mətn bütün şəxsi söhbətlərinizə atılar'
).add_command(
    'unvoice', 'musiqiyə cavab olaraq', 'Cavab verdiyiniz musiqini səsli mesaja çevirir'
).add_command(
    'status', None, 'Hesabınızda məlumat və statistikanı sizə təqdim edər (count modulu ilə qarışdırmayın).'
).add_command(
    'gsend', '<qrup linki> <mesajınız>', 'İstədiyiniz qrupa qoşulmadan mesaj yazın.'
).add_command(
    'oxu', '<fayla cavab olaraq>', 'Faylı mətnə çevirin'
).add_command(
    'fayl', '<mətnə cavab olaraq>', 'Mətni fayl sonluğu artıraraq istədiyiniz növ fayla çevirin'
).add()
