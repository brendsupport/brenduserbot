# Eken bize ata desin
# Ne baxirsan?
# Oğurlamaq = övladımız olmaq
# Copying is the cause of swearing

import os, random, asyncio
from userbot.events import register
from userbot import CMD_HELP, bot, SUP
from telethon.tl.types import ChannelParticipantsAdmins as cp
from userbot.main import PLUGIN_MESAJLAR
from time import sleep
from userbot.cmdhelp import CmdHelp

vaxt = int(PLUGIN_MESAJLAR['tagsleep'])

@register(outgoing=True, groups_only=True, pattern="^.tagone(?: |$)(.*)")
async def tagone(tag):
    if tag.chat_id in SUP:
        return await tag.edit("**Mən Brend Support qrupunda tag başlada bilmərəm!!!**")
    if tag.pattern_match.group(1):
        seasons = tag.pattern_match.group(1)
    else:
        seasons = ""
    chat = await tag.get_input_chat()
    a_=0
    await tag.delete()
    async for i in bot.iter_participants(chat):
        if a_ == 500:
                break
        a_+=5
        await tag.client.send_message(tag.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, seasons))
        sleep(vaxt)
	
		
@register(outgoing=True, groups_only=True, pattern="^.admins(?: |$)(.*)")
async def _(tagadmin):
    if tagadmin.chat_id in SUP:
        return await tagadmin.edit("**Mən Brend Support qrupunda tag başlada bilmərəm!!!**")	
    if tagadmin.pattern_match.group(1):
        seasons = tagadmin.pattern_match.group(1)
    else:
        seasons = ""
    chat = await tagadmin.get_input_chat()
    a_=0
    await tagadmin.delete()
    async for i in bot.iter_participants(chat, filter=cp):
        if a_ == 500:
                break
        a_+=5
        await tagadmin.client.send_message(tagadmin.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, seasons))
        sleep(vaxt)


@register(outgoing=True, groups_only=True, pattern="^.all$")
async def _(event):
    if event.chat_id in SUP:
        return await event.edit("**Mən Brend Support qrupunda tag başlada bilmərəm!!!**")
    if event.fwd_from:
        return
    mentions = "@all"
    chat = await event.get_input_chat()
    leng = 0
    async for x in bot.iter_participants(chat):
        if leng < 4092:
            mentions += f"[\u2063](tg://user?id={x.id})"
            leng += 1
    await event.reply(mentions)
    await event.delete()
	

emoji = " ♥️ ♠️ ♣️ 🎴 🃏 💸 💰 💎 🧨 💣 🛡 🔫 🔮 🚬 🎈 🎸🎲 🎭 🍾 🥂 🍻 🧃 🍯 🍭 " \
  " 🍬 🎂 🍒 🍓 🍇 🔥 🌪 🥀 🌹 🌸 🐇 🦜 🦩 🐠 🐬 🐝 🐣".split(" ")


class FlagContainer:
    is_active = False


#eken peyserdi
#eken bize bir basa ata desin
@register(outgoing=True, groups_only=True, pattern="^.etag.*")
async def b(event):
    if event.chat_id in SUP:
        return await event.edit("**Mən Brend Support qrupunda tag başlada bilmərəm!!!**")
    if event.fwd_from or FlagContainer.is_active:
        return
    try:
        FlagContainer.is_active = True
        text = None
        args = event.message.text.split(" ", 1)
        if len(args) > 1:
            text = args[1]
        chat = await event.get_input_chat()
        await event.delete()
        tags = list(map(lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})", await event.client.get_participants(chat)))
        current_pack = []
        async for participant in event.client.iter_participants(chat):
            if not FlagContainer.is_active:
                break
            current_pack.append(participant)
            if len(current_pack) == 5:
                tags = list(map(lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})", current_pack))
                current_pack = []
                if text:
                    tags.append(text)
                await event.client.send_message(event.chat_id, " ".join(tags))
                await asyncio.sleep(vaxt)
    finally:
        FlagContainer.is_active = False

@register(outgoing=True, groups_only=True, pattern="^.stoptag")
async def m_fb(event):
    if event.fwd_from or not FlagContainer.is_active:
        return
    await event.delete()
    FlagContainer.is_active = False

# ekme serefsiz
# oğurlayanin anasini bacsıni sikim
# ekenin varyoxunu onun boynunda sikim.

muveqqeti_isleyen = []

@register(outgoing=True, groups_only=True, pattern="^.tagall(?: |$)(.*)")
async def tagall(event):
  global muveqqeti_isleyen
  if event.chat_id in SUP:
    return await event.edit("**Mən Brend Support qrupunda tag başlada bilmərəm!!!**")
  await event.delete()
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Köhnə mesajlardakı istifadəçiləri çağıra bilmərəm! (köhnə mesajlar mən qrupa gəlməzdən əvvəl olan mesajlardır)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Mənə bir mesaj ver__")
  else:
    return await event.respond("__Bir mesaja cavab verin və ya əmrin yanına səbəb yazın__")
    
  if mode == "text_on_cmd":
    muveqqeti_isleyen.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in event.client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in muveqqeti_isleyen:
        await event.respond("❌Proses müvəffəqiyyətlə dayandırıldı!")
        return
      if usrnum == 5:
        await event.client.send_message(event.chat_id, f"{msg}\n\n{usrtxt}")
        await asyncio.sleep(vaxt)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    muveqqeti_isleyen.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in event.client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in muveqqeti_isleyen:
        await event.respond("❌Proses müvəffəqiyyətlə dayandırıldı")
        return
      if usrnum == 5:
        await event.client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(vaxt)
        usrnum = 0
        usrtxt = ""
	
        
@register(outgoing=True, groups_only=True, pattern="^.canceltag")
async def cancel(event):
  global muveqqeti_isleyen
  await event.delete()
  muveqqeti_isleyen.remove(event.chat_id)


@register(outgoing=True, pattern="^.tag(?: |$)(.*)")
async def taginfo(event):
    await event.edit("⚡ Brend Userbotun tag modulu çox təkmilləşdirildi. Daha çoxu üçün `.brend tagger` yazın")


CmdHelp('tagger').add_command(
    'tagone', '<səbəb>', 'Qrupdakı userləri tək-tək tağ edər'
).add_command(
    'admins', '<səbəb>', 'Qrupdakı adminləri tək-tək tag edər'
).add_command(
    'etag', '<səbəb>', 'Qrupdakı userləri emojilərlə tag edər.'
).add_command(
    'all', '', 'Qrupdakı userləri tək bir mesajda tag edər.'
).add_command(
    'stoptag', None, 'etag prosesini saxlayar.'
).add_command(
    'tagall', '<səbəb> və ya <cavablamaq>', 'Qrupdakı userləri 5-5 tağ edər'
).add_command(
    'canceltag', None, '5-5 tag prosesini dayandırar'
).add()
