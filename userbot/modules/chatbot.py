import requests
from googletrans import Translator
from telethon.tl.types import User
from userbot import CMD_HELP, LOGS
from userbot.events import register
from userbot.modules.sql_helper.brend_chatbot_sql import brend, userbot, chatbot

translator = Translator()
LANGUAGE = "az"

url = "https://apitede.herokuapp.com/api/chatbot?message={message}"


async def sozler(message):
    bir_link = url.format(message=message)
    try:
        data = requests.get(bir_link)
        if data.status_code == 200:
            return (data.json())["msg"]
        LOGS.info("XƏTA: Chatbot API işləmir, @BrendSUP-a məlumat verin.")
    except Exception as e:
        LOGS.info(str(e))


async def aktivlesme(event):
    status = event.pattern_match.group(1).lower()
    chat_id = event.chat_id
    if status == "on":
        if not brend(chat_id):
            userbot(chat_id)
            return await event.edit("**ChatBot Uğurla Aktiv edildi!**")
        await event.edit("ChatBot Artıq Aktivləşdirilib.")
    elif status == "off":
        if brend(chat_id):
            chatbot(chat_id)
            return await event.edit("**ChatBot Uğurla Deaktiv edildi!**")
        await event.edit("ChatBot Deaktiv edilib.")
    else:
        await event.edit("**İstifadəsi:** `.chatbot` <on/off>")


@register(outgoing=True, pattern="^.chatbot(?: |$)(.*)")
async def on_off(event):
    await aktivlesme(event)


@register(incoming=True, func=lambda e: (e.mentioned))
async def tede_chatbot(event):
    sender = await event.get_sender()
    if not brend (event.chat_id):
        return
    if not isinstance(sender, User):
        return
    if event.text:
        rep = await sozler(event.message.message)
        tr = translator.translate(rep, LANGUAGE)
        if tr:
            await event.reply(tr.text)
