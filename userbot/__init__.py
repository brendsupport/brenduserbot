import os
from re import compile
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from requests import get
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.events import callbackquery, InlineQuery, NewMessage
from math import ceil

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(format="%(asctime)s - @BrendUserBot - %(levelname)s - %(message)s", level=DEBUG)
else:
    basicConfig(format="%(asctime)s - @BrendUserBot - %(levelname)s - %(message)s",  level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info("Ən azı python 3.9 versiyanız olmalıdır."
              "Birdən çox xüsusiyyət bundan asılıdır. Bot bağlanır.")
    quit(1)
    
BREND_VERSION = "v5"
API_ID = int(os.environ.get("API_KEY", "1558926"))
API_HASH = os.environ.get("API_HASH", "69c4c16e17e9f637818f2cfce8f9bce5")
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# LOG Group
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID") or 0)
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))
PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

# Heroku
HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "True"))
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///brend.db")

WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")
if not WARN_MODE in ["gmute", "gban"]:
    WARN_MODE = "gmute"

PLUGIN_ID = os.environ.get("PLUGIN_ID", "me")
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))
PATTERNS = os.environ.get("PATTERNS", ".")

CMD_HELP = {}
CMD_HELP_BOT = {}

LANGUAGE = os.environ.get("LANGUAGE", "DEFAULT").upper()
if not LANGUAGE in ["AZ"]:
    LOGS.info("Naməlum bir dil yazdınız. Buna görə DEFAULT istifadə olunur.")
    LANGUAGE = "AZ"

WHITELIST = get('https://gitlab.com/brenduserbot/brend-userbot/-/raw/master/whitelist.json').json()
SUPPORT = get('https://gitlab.com/brenduserbot/brend-userbot/-/raw/master/support.json').json()
HUSU = get('https://gitlab.com/brenduserbot/brend-userbot/-/raw/master/husu.json').json()

SUP = [-1001197418406]
BRAIN_CHECKER = []

if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
else:
    bot = TelegramClient("brend", API_ID, API_HASH)

if os.path.exists("brend.check"):
    os.remove("brend.check")
else:
    LOGS.info("Brain check faylı yoxdur, alınır...")

URL = 'https://gitlab.com/brenduserbot/brend-userbot/-/raw/master/brend.check'
with open('brend.check', 'wb') as load:
    load.write(get(URL).content)

async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info("LogSpammer özəlliyinin aktivləşməsi üçün BOTLOG_CHATID dəyərini doldurmalısınız.")
        quit(1)
    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info("BOTLOG özəlliyini aktiv etmək üçün BOTLOG_CHATID dəyərini doldurun.")
        quit(1)
    elif not BOTLOG or not LOGSPAMMER:
        return
    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info("Hesabınızla BOTLOG_CHATID qrupuna mesaj göndərmək olmurş/nQrup ID-sini düzgün yazdığınızdan əmin olun.")
        quit(1)
        
if not BOT_TOKEN == None:
    tgbot = TelegramClient("Brend_Bot",api_id=API_ID, api_hash=API_HASH).start(bot_token=BOT_TOKEN)
else:
    tgbot = None

def butonla(sehife, modullar):
    Setir = 5
    Kalon = 2
    global looters
    looters = sehife
    modullar = sorted([modul for modul in modullar if not modul.startswith("_")])
    pairs = list(map(list, zip(modullar[::2], modullar[1::2])))
    if len(modullar) % 2 == 1:
        pairs.append([modullar[-1]])
    max_pages = ceil(len(pairs) / Setir)
    pairs = [pairs[i:i + Setir] for i in range(0, len(pairs), Setir)]
    butonlar = []
    for pairs in pairs[sehife]:
        butonlar.append([custom.Button.inline("⚡ " + pair, data=f"bilgi[{sehife}]({pair})") for pair in pairs])
    butonlar.append([custom.Button.inline("👈🏻 Geri", data=f"sehife({(max_pages - 1) if sehife == 0 else (sehife - 1)})"), custom.Button.inline("❎ Bağla ❎", data="close"), custom.Button.inline("İləri 👉🏻", data=f"sehife({0 if sehife == (max_pages - 1) else sehife + 1})")])
    return [max_pages, butonlar]

with bot:
    try:
        bot(JoinChannelRequest("@BrendUserbot"))
        bot(JoinChannelRequest("@BrendSupport"))
    except:
        pass

    modullar = CMD_HELP
    me = bot.get_me()
    uid = me.id
    BREND_USERNAME = bot.get_me()
    ALIVE_NAME = f"{me.first_name}"
    DEFAULT_NAME = f"{me.first_name}"
    SAHIB = me.id
    BREND_MENTION = f"[{DEFAULT_NAME}](tg://user?id={SAHIB})"
    helplogo = "https://telegra.ph/file/92494510fe2b53d30492c.gif"

    try:
        @tgbot.on(NewMessage(pattern='/start'))
        async def helpstart(event):
            if not event.message.from_id == uid:
                await event.reply(f'Salam mən @BrendUserbot Assistant!\nMən {BREND_MENTION} üçün hazırlanmışam, yəni sənə kömək edə bilmərəm.\nAmma sən də öz hesabına [Brend Userbot](t.me/BrendUserbot) qura bilərsən.')
            else:
                await event.reply(f'Salam {DEFAULT_NAME}!\nBrend Köməkçi aktivdir.')
                                  
        @tgbot.on(InlineQuery)  
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("@BrendUserbot"):
                rev_text = query[::-1]
                veriler = (butonla(0, sorted(CMD_HELP)))
                result = builder.photo(
                    file=helplogo,
                    link_preview=False, 
                    text=f"**⚡ 𝐁𝐫𝐞𝐧𝐝 𝐔𝐬𝐞𝐫𝐛𝐨𝐭​**\n\n**📥 Yüklənən modul sayı:** `{len(CMD_HELP)}`\n**📄 Səhifə:** 1/{veriler[0]}", 
                    buttons=veriler[1])
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article("@Brend", text=f"**📂 Fayl uğurla {parca[2]} saytına yükləndi!**\n\n⏱️ Yükləmə müddəti: {parca[1][:3]} saniyə\n[‏‏‎hmm]({parca[0]})", buttons=[[custom.Button.url('URL', parca[0])]], link_preview=True)
            else:
                result = builder.article("@BrendUserbot", text="@BrendUserbot işlətməyi yoxlayın! Sizdə Hesabınıza bot qurub istifadə edə bilərsiniz.", buttons=[[custom.Button.url("⚡ Brend Userbot", "https://t.me/BrendUserBot"), custom.Button.url("Dəstək Qrupu 👨🏻‍🔧", "https://t.me/BrendSUP")], [custom.Button.url("📨 Plugin Kanalı 📢", "https://t.me/BrendPlugin")]], link_preview=False)
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"sehife\((.+?)\)")))
        async def sehife(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarıma toxunma! Öz hesabına @BrendUserbot qur.", cache_time=0, alert=True)
            sehife = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonla(sehife, CMD_HELP)
            text = f"**⚡ 𝐁𝐫𝐞𝐧𝐝 𝐔𝐬𝐞𝐫𝐛𝐨𝐭​**\n\n**📥 Yüklənən modul sayı:** `{len(CMD_HELP)}`\n**📄 Səhifə:** {sehife + 1}/{veriler[0]}"
            await event.edit(text, file=helplogo, buttons=veriler[1], link_preview=False)
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(rb"ofen")))
        async def ofen(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarıma toxunma! Öz hesabına @BrendUserbot qur.", cache_time=0, alert=True)
            sehife = int(looters)
            veriler = butonla(sehife, CMD_HELP)
            text = f"**⚡ 𝐁𝐫𝐞𝐧𝐝 𝐔𝐬𝐞𝐫𝐛𝐨𝐭​**\n\n**📥 Yüklənən modul sayı:** `{len(CMD_HELP)}`\n**📄 Səhifə:** {sehife + 1}/{veriler[0]}"
            await event.edit(text, file=helplogo,  buttons=veriler[1],  link_preview=False)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
        async def sehife(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarıma toxunma! Öz hesabına @BrendUserbot qur.", cache_time=0, alert=True)
            buttons =[[custom.Button.inline("Menyunu aç", data="ofen")]]
            await event.edit("Menyu bağlandı", buttons=buttons)


        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarıma toxunma! Öz hesabına @BrendUserbot qur.", cache_time=0, alert=True)
            sehife = int(event.data_match.group(1).decode("UTF-8"))
            emr = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("💎 " + cmd[0], data=f"emr[{emr}[{sehife}]]({cmd[0]})") for cmd in CMD_HELP_BOT[emr]['commands'].items()]
            except KeyError:
                return await event.answer("❌ Bu modula açıqlama yazılmayıb.", cache_time=0, alert=True)
            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("👈🏻 Geri", data=f"sehife({sehife})")])
            await event.edit(f"**📂 Fayl:** `{emr}`\n**🔢 Əmr sayı:** `{len(CMD_HELP_BOT[emr]['commands'])}`", file=helplogo, buttons=butonlar, link_preview=False)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"emr\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def emr(event):
            if not event.query.user_id == uid: 
                return await event.answer("❌ Hey! Mənim mesajlarıma toxunma! Öz hesabına @BrendUserbot qur.", cache_time=0, alert=True)
            cmd = event.data_match.group(1).decode("UTF-8")
            sehife = int(event.data_match.group(2).decode("UTF-8"))
            emr = event.data_match.group(3).decode("UTF-8")
            result = f"**🗂️ Fayl:** `{cmd}`\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️ Diqqət:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️ Rəsmi:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️ Diqqət:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"
            command = CMD_HELP_BOT[cmd]['commands'][emr]
            if command['params'] is None:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠 Əmr:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
            if command['example'] is None:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n\n"
            else:
                result += f"**💬 Açıqlama:** `{command['usage']}`\n"
                result += f"**⌨️ Nümunə:** `{PATTERNS[:1]}{command['example']}`\n\n"
            await event.edit(result, file=helplogo, buttons=[custom.Button.inline("👈🏻 Geri", data=f"bilgi[{sehife}]({cmd})")], link_preview=False)
    except Exception as e:
        print(e)
        LOGS.info(f"Botunuzda inline rejimi deaktivdir./nAktivləşdirmək üçün botunuzda inline rejimini aktivləşdirin./nBunun xaricində bir problem olduğunu düşünürsünüzsə, dəstək qrupumla əlaqə saxlayın. @BrendSUP/n/n{e}")
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info("BOTLOG_CHATID yeniləməyiniz tövsiyyə olunur.")
        quit(1)
