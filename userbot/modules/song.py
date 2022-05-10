import asyncio, os, json, base64
from requests import get
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import bot, CMD_HELP, DEFAULT_NAME
from userbot.events import register
from random import randint
from userbot.cmdhelp import CmdHelp
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import ContentTooShortError, DownloadError, ExtractorError, GeoRestrictedError, MaxDownloadsReached, PostProcessingError, UnavailableVideoError, XAttrMetadataError
from youtube_search import YoutubeSearch
from userbot.language import get_value
LANG = get_value("song")

@register(outgoing=True, pattern="^.deez(\d*|)(?: |$)(.*)")
async def deezl(event):
    if event.fwd_from:
        return
    sira = event.pattern_match.group(1)
    if sira == '':
        sira = 0
    else:
        sira = int(sira)
    mahni = event.pattern_match.group(2)
    if len(mahni) < 1:
        if event.is_reply:
            sarki = await event.get_reply_message().text
        else:
            await event.edit(LANG['GIVE_ME_SONG']) 
    await event.edit(LANG['SEARCHING'])
    chat = "@DeezerMusicBot"
    async with bot.conversation(chat) as conv:
        try:     
            mesaj = await conv.send_message(str(randint(31,62)))
            mahnilar = await conv.get_response()
            await mesaj.edit(mahni)
            mahnilar = await conv.get_response()
        except YouBlockedUserError:
            await event.reply(LANG['BLOCKED_DEEZER'])
            return
        await event.client.send_read_acknowledge(conv.chat_id)
        if mahnilar.audio:
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, LANG['UPLOADED_WITH'], file=mahnilar.message)
            await event.delete()
        elif mahnilar.buttons[0][0].text == "No results":
            await event.edit(LANG['NOT_FOUND'])
        else:
            await mahnilar.click(sira)
            mahni = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, f"`{mahnilar.buttons[sira][0].text}` | " + LANG['UPLOADED_WITH'], file=mahni.message)
            await event.delete()

@register(outgoing=True, pattern=r"^.song (.*)")
async def mahniyukle(event):
    a = event.text
    if len(a) >= 5 and a[5] == "s":
        return
    await event.edit("🔎Musiqi axtarılır, xahiş edirəm bir az gözləyin...")
    url = event.pattern_match.group(1)
    if not url:
        return await event.edit("**❌ Axtarış Xətası**\n\n✍🏻 İstifadə qaydası: -`.song Aşıl Empati`")
    results = []
    results = YoutubeSearch(url, max_results=1).to_dict()
    try:
        url = f"https://youtube.com{results[0]['url_suffix']}"
    except BaseException:
        return await event.edit("🤦🏻‍♂️ Mahnını tapa bilmirəm...")
    type = "audio"
    await event.edit(f"📥 Hazırdır Endirilir...")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.m4a",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await event.edit("🔄 Musiqi məlumatı əldə olunur...")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"{DE}")
        return
    except ContentTooShortError:
        await event.edit("😬 Endirmə məzmunu çox qısa idi.")
        return
    except GeoRestrictedError:
        await event.edit("🥸 Olduğunuz ölkənin şəbəkəsində bu mahnı mövcud deyil bir veb sayt məhdudiyyət qoyub")
        return
    except MaxDownloadsReached:
        await event.edit("☹️ Maksimum yükləmə limitinə çatıdınız.")
        return
    except PostProcessingError:
        await event.edit("🙄 Musiqini hazırlayarkən xəta baş verdi")
        return
    except UnavailableVideoError:
        await event.edit("🤦🏻‍♂️ İstədiyiniz mahnını musiqi formatında tapa bilmədim")
        return
    except XAttrMetadataError as XAME:
        return await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await event.edit("❌ Musiqini yükləyərkən xəta baş verdi")
    except Exception as e:
        return await event.edit(f"{str(type(e)): {str(e)}}")
    dir = os.listdir()
    if f"{rip_data['id']}.m4a.jpg" in dir:
        thumb = f"{rip_data['id']}.m4a.jpg"
    elif f"{rip_data['id']}.m4a.webp" in dir:
        thumb = f"{rip_data['id']}.m4a.webp"
    else:
        thumb = "userbot/modules/sql_helper/resources/Brend_Logo.jpg"
    await event.edit(f"📥 Yüklənir...\n• 🎶 Mahnı: {rip_data['title']}\n• 📡 Kanal: {rip_data['uploader']}")
    CAPT = f"╰┈───────────────┈╮\n➥ 🎵 {rip_data['title']}\n➥ 📡 Kanal: {rip_data['uploader']}\n╭┈───────────────┈╯\n➥ 👤 Sahibim: {DEFAULT_NAME}\n╰┈───────────────┈➤"
    await event.delete()
    await event.client.send_file(
        event.chat_id,
        f"{rip_data['id']}.m4a",
        thumb=thumb,
        supports_streaming=True,
        caption=CAPT,
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    os.remove(f"{rip_data['id']}.m4a")
    try:
        os.remove(thumb)
    except BaseException:
        pass

@register(outgoing=True, pattern=r"^.lyrics (.*)")
async def lyrics(event):
    query = event.pattern_match.group(1)
    if not query:
        return await event.edit("**Zəhmət olmasa mahnının adını daxil edin**")
    try:
        await event.edit("`Mahnı sözləri axtarılır...`")
        respond = requests.get(f"https://api-tede.herokuapp.com/api/lirik?l={query}").json()
        result = f"{respond['data']}"
        await event.edit(result)
    except Exception:
        await event.edit("**Mahnının sözləri tapılmadı.**")


CmdHelp('song').add_command(
    'deez', '<mahnı adı>', 'Deezerdən mahnı atar.'
).add_command(
    'song', '<mahnı adı>', 'Mahnı yükləyər.'
).add_command(
    'lyrics', '<mahnı adı>', 'Mahnının sözlərini axtarar'
).add()
