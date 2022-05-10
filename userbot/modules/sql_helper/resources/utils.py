import asyncio, sys, heroku3
from random import randint
from telethon.tl.functions.contacts import UnblockRequest
from userbot import BOT_TOKEN, HEROKU_APIKEY, HEROKU_APPNAME, bot, me as b

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None

async def brendautobot():
    if BOT_TOKEN:
        return
    await bot.start()
    await asyncio.sleep(15)
    await bot.send_message(b, "**@BotFather-də sizin üçün Telegram Assistant bot alınır**")
    brend = await bot.get_me()
    adi = f"{brend.first_name}"
    if brend.username:
        username = f"{brend.username}_{randint(1, 1000)}_bot"
    else:
        username = f"brend{(str(brend.id))[5:]}bot"
    bf = "@BotFather"
    await bot(UnblockRequest(bf))
    await bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/start")
    await asyncio.sleep(1)
    await bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do."):
        await bot.send_message(b, "@BotFather dən bot yaradıb tokenini herokuda BOT_TOKEN-ə əlavə edin")
        sys.exit(1)
    await bot.send_message(bf, f"{adi} Assistant")
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            await bot.send_message("Lütfən, @BotFather-dən Bot yaradın və onun işarəsini BOT_TOKEN-ə əlavə edin")
            sys.exit(1)
    await bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await bot.get_messages(bf, limit=1))[0].text
    await bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = f"brend{(str(brend.id))[6:]}{str(ran)}bot"
        await bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            await bot.send_message(bf, "/setinline")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, "Search")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setabouttext")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"☕️ {adi} üçün yaradılmışam")
            await asyncio.sleep(3)
            await bot.send_message(bf, "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"@{username}")
            await asyncio.sleep(1)
            await bot.send_message(bf, f"✨ Sahib ~ {adi} ✨\n\n⚡ Powered By ~ @BrendUserbot ⚡")
            await bot.send_message(b, f"**İstifadəçi Adı @{username} olan telegram botu uğurla tamamlandı**",)
            heroku_var["BOT_USERNAME"] = username
            heroku_var["BOT_TOKEN"] = token
        else:
            await bot.send_message("Lütfən, @Botfather ünvanında Telegram Botlarınızdan bəzilərini silin və ya bot nişanları ilə Var BOT_TOKEN təyin edin")
            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        await bot.send_message(bf, "/setinline")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, "Search")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setabouttext")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"☕️ {adi} üçün yaradılmışam")
        await asyncio.sleep(3)
        await bot.send_message(bf, "/setdescription")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"@{username}")
        await asyncio.sleep(1)
        await bot.send_message(bf, f"👑 Sahib ~ {adi} 👑\n\n⚡ Powered By ~ @BrendUserbot ⚡")
        heroku_var["BOT_USERNAME"] = username
        heroku_var["BOT_TOKEN"] = token
    else:
        await bot.send_message(b, "Lütfən, @Botfather ünvanında Telegram Botlarınızdan bəzilərini silin və ya bot nişanları ilə Var BOT_TOKEN təyin edin")
        sys.exit(1)
