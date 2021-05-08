import datetime
import asyncio
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register
import os
import subprocess
import glob
from random import randint
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("song")


# Originally from Bothub
# Port to UserBot by @heyworld
#Copyright (C) 2020 azrim.
#imported .song and .vsong form catuserbot

from telethon import events
import asyncio
import glob
import shutil
from userbot.events import register
from userbot import bot, CMD_HELP, GOOGLE_CHROME_BIN, TEMP_DOWNLOAD_DIRECTORY, bot
from telethon.errors.rpcerrorlist import YouBlockedUserError
import os
import subprocess
import time
from asyncio.exceptions import TimeoutError
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pylast import User
from selenium import webdriver
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from userbot.utils import progress
import pybase64

async def brendmusic(cat, QUALITY, hello):
    search = cat
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--test-type")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.youtube.com/results?search_query=" + search)
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        video_link = i.get_attribute("href")
        break
    if not os.path.isdir("./temp/"):
        os.makedirs("./temp/")
    if not video_link:
        await hello.edit(f"Bağışlayın. `{search}` mahnısını tapa bilmirəm ")
        return
    try:
        command = (
            'youtube-dl -o "./temp/%(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality '
            + QUALITY
            + " "
            + video_link
        )
        os.system(command)
    except Exception as e:
        return await hello.edit(f"`Xəta:\n {e}`")
    try:
        thumb = (
            'youtube-dl -o "./temp/%(title)s.%(ext)s" --write-thumbnail --skip-download '
            + video_link
        )
        os.system(thumb)
    except Exception as e:
        return await hello.edit(f"`Xəta:\n {e}`")


@register(outgoing=True, pattern="^.deez(\d*|)(?: |$)(.*)")
async def deezl(event):
    if event.fwd_from:
        return
    sira = event.pattern_match.group(1)
    if sira == '':
        sira = 0
    else:
        sira = int(sira)

    sarki = event.pattern_match.group(2)
    if len(sarki) < 1:
        if event.is_reply:
            sarki = await event.get_reply_message().text
        else:
            await event.edit(LANG['GIVE_ME_SONG']) 

    await event.edit(LANG['SEARCHING'])
    chat = "@DeezerMusicBot"
    async with bot.conversation(chat) as conv:
        try:     
            mesaj = await conv.send_message(str(randint(31,62)))
            sarkilar = await conv.get_response()
            await mesaj.edit(sarki)
            sarkilar = await conv.get_response()
        except YouBlockedUserError:
            await event.reply(LANG['BLOCKED_DEEZER'])
            return
        await event.client.send_read_acknowledge(conv.chat_id)
        if sarkilar.audio:
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, LANG['UPLOADED_WITH'], file=sarkilar.message)
            await event.delete()
        elif sarkilar.buttons[0][0].text == "No results":
            await event.edit(LANG['NOT_FOUND'])
        else:
            await sarkilar.click(sira)
            sarki = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, f"`{sarkilar.buttons[sira][0].text}` | " + LANG['UPLOADED_WITH'], file=sarki.message)
            await event.delete()

@register(outgoing=True, pattern="^.song(?: |$)(.*)")
async def _(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.messag
    else:
        event = await event.edit("`Nə tapmalıyam? `")
        return
    event = await event.edit("`Hey...! Sənin mahnını tapıram....`")
    await brendmusic(str(query), "128k", event)
    l = glob.glob("./temp/*.mp3")
    if l:
        await event.edit("Mahnını tapdım yükləyirəm...📥")
    else:
        await event.edit(f"Bağışlayın ..! `{query}` ilə bir şey tapa bilmirəm")
        return
    thumbcat = glob.glob("./temp/*.jpg") + glob.glob("./temp/*.webp")
    if thumbcat:
        catthumb = thumbcat[0]
    else:
        catthumb = None
    loa = l[0]
    await bot.send_file(
        event.chat_id,
        loa,
        force_document=False,
        allow_cache=False,
        caption=query,
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await event.delete()
    os.system("rm -rf ./temp/*.mp3")
    os.system("rm -rf ./temp/*.jpg")
    os.system("rm -rf ./temp/*.webp")



@register(outgoing=True, pattern="^.songu(?: |$)(.*)")
async def port_song(event):
    if event.fwd_from:
        return
    
    cmd = event.pattern_match.group(1)
    if len(cmd) < 1:
        await event.edit(LANG['UPLOADED_WITH']) 

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
        
    await event.edit(LANG['SEARCHING_SPOT'])  
    dosya = os.getcwd() 
    os.system(f"spotdl --song {cmd} -f {dosya}")
    await event.edit(LANG['DOWNLOADED'])    

    l = glob.glob("*.mp3")
    if len(l) >= 1:
        await event.edit(LANG['UPLOADING'])
        await event.client.send_file(
            event.chat_id,
            l[0],
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id
        )
        await event.delete()
    else:
        await event.edit(LANG['NOT_FOUND'])   
        return 
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)

@register(outgoing=True, pattern="^.songpl ?(.*)")
async def songpl(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)

    if len(cmd) < 1:
        await event.edit(LANG['USAGE_PL'])    

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit(LANG['SEARCHING_PL'])
    dosya = os.getcwd() + "/playlist/" + "pl.pl"
    klasor = os.getcwd() + "/playlist/"
    sonuc = os.system(f"spotdl --playlist {cmd} --write-to=\"{dosya}\"")
    sonuc2 = os.system(f"spotdl --list {dosya} -f {klasor}")
    await event.edit(LANG['DOWNLOADED'])
    l = glob.glob(f"{klasor}/*.mp3")
    i = 0
    if len(l) >= 1:
        while i < len(l):
            await event.reply(LANG['SENDING_SONGS'] + l[i])
            await event.client.send_file(
                event.chat_id,
                l[i],
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
    else:
        await event.edit(LANG['NOT_FOUND_PL'])   
        return 
    os.system(f"rm -rf {klasor}/*.mp3")
    subprocess.check_output(f"rm -rf {klasor}/*.mp3",shell=True)
    os.system(f"rm -rf {klasor}/*.pl")
    subprocess.check_output(f"rm -rf {klasor}/*.pl",shell=True)

CmdHelp('song').add_command(
    'deez', '<mahnı adı/youtube/spotify/soundcloud>', 'Bir neçə saytdan axtararaq, mahnı atar.'
).add_command(
    'song', '<mahnı adı/youtube/spotify>', 'Mahnı yükləyər.'
).add_command(
    'songpl', '<spotify playlist>', 'Spotify Playlist\'indən mahnı yükləyər'
).add()
