# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

from asyncio import sleep
from random import choice, getrandbits, randint
from re import sub
import time
import asyncio

from collections import deque

import requests

from cowpy import cow

from userbot import CMD_HELP, ZALG_LIST
from userbot.events import register
from userbot.modules.admin import get_user_from_event
from userbot.cmdhelp import CmdHelp

# ================= CONSTANT =================
EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNS_STR = [
    "Hey! Hara gedirsən?"
    "Hə? Nə? Qaçdılar?"
    "ZZzzZZzz ... Nə oldu? yenə onlardır, heç düşünməyin.",
    "Geri qayıt!",
    "OneBot-un gəlməsindən çəkinin!",
    "Divara diqqət yetirin!",
    "Məni onlarla tək qoyma !!",
    "Qaçsan ölərsən.",
    "Zarafat edirsən, mən hər yerdəyəm.",
    "Bunu etdiyinizə görə peşman olacaqsınız ...",
    "/Kickme düyməsini də sınaya bilərsiniz, əyləncəli olduğunu söyləyirlər.",
    "Get başqasını narahat et, burada heç kimin vecinə deyil.",
    "Qaça bilərsən, ancaq gizlənə bilməzsən.",
    "Nə edə bilərsən?",
    "Sənin arxasındayam ...",
    "Qonaqlarınız var!",
    "Bunu asanlıqla və ya çətin bir şəkildə edə bilərik.",
    "Sən başa düşmürsən, elə deyilmi?",
    "Haha, daha yaxşı qaçsan!",
    "Xahiş edirəm, mənə nə qədər əhəmiyyət verdiyimi xatırlat?",
    "Mən sizin yerinizdə olsaydım daha sürətli qaçardım.",
    "Bu mütləq axtardığımız robot.",
    "Bəlkə şans sizə güləcək.",
    "Məşhur son sözlər.",
    "Və sonsuza qədər yox oldular, heç görmədilər.",
    "Bəli bəli, indi / kick düyməsini basın.",
    "Budur, bu üzüyü götür və Mordora get.",
    "Rəvayətə görə hələ də işləyirlər ...",
    "Harry Potter'dan fərqli olaraq, valideynləriniz sizi məndən qoruya bilməzlər.",
    "Qorxu qəzəbə, qəzəb nifrətə, nifrət ağrıya aparar. Qorxu içində qaçmağa davam etsən"
    "Siz növbəti Vader ola bilərsiniz.",
    "Çox hesablama apardıqdan sonra fəndlərə marağımın tam 0 olduğuna qərar verdim."
    "Əfsanə hələ də çalışdıqlarını söylədi."
    "Davam et, səni burada istədiyimizə əmin deyiləm.",
    "Sən sehrbazsan - Oh. Gözlə. Harry deyilsən, davam et.",
    "Dəhlizdə qaçma!",
    "Görüşək balam.",
    "İtləri kim çölə buraxdı?"
    "Gülməli, çünki heç kimin vecinə deyil.",
    "Oh, nə itki. Mən bunu sevirdim.",
    "Açığı canım, vecimə deyil.",
    "Südüm bütün kişiləri həyətə çəkir ... Daha sürətli qaç!",
    "Həqiqəti silə bilməzsən!",
    "Çoxdan əvvəl kimsə onu çox uzaq bir qalaktikada taxa bilərdi. Ancaq artıq yox.",
    "Hey, onlara bax! Qaçılmaz banhammerdən qaçırlar ... Nə qədər sevimli",
    "Inn əvvəl vuruldu. Bunu edəcəm",
    "Ağ dovşanın arxasında nə edirsən?",
    "Doktorunun dediyi kimi ... CACHE!",
]

HELLOSTR = [
    "Salam var!",
    "Necəsən'?",
    "'Hey nə baş verir?",
    "Salam, salam, salam!",
    "Salam, kim var? Mən danışıram.",
    "Bunun kim olduğunu bilirsiniz",
    "Hey Yo!"
    "Nə var nə yox.",
    "Salam salam salam!",
    "Salam, günəş işığı!",
    "Hey, nə var, salam!",
    "Necə gedir balaca cücə?"
    "Nə yaxşıdır!"
    "Salam, birinci sinif brat!",
    "Gəl barışaq!",
    "Salam dostum!",
    "Salam!",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES = [
    "{victim} istifadəçisini {item} ilə {hits} .",
    "{victim} istifadəçisini {item} ilə yüzünə {hits} .",
    "{victim} istifadəçisini {item} ilə biraz {hits} .",
    "{victim} istifadəçisini {item} {throws} .",
    "{victim} istifadəçisini {item} ile yüzünə {throws} .",
    "{victim} istifadəçisiyi doğru {item} fırlatıyor.",
    "{victim} xəstəsinə {item} ilə döyür.",
    "{victim} istifadəçisini yerə sərib ard arda {item} ilə {hits} .",
    "{item} alaraq {victim} {hits}.",
    "{victim} istifadəçisini kresloya bağlayıb {item} {throws} .",
    "{victim} istifadəçisinə lava basaraq onu lava ilə üzməyi öyrənməyə imkan verir."
]

ITEMS = [
    "dəmir qazan",
    "böyük alabalıq",
    "beysbol sopası",
    "cricket yarasa",
    "taxta çubuq",
    "dırnaq",
    "Printer",
    "kürək",
    "boru monitoru",
    "fizika kitabı",
    "toster",
    "Richard Stallmanın portreti",
    "televiziya",
    "beş tonluq yük maşını",
    "Kanal lenti",
    "kitab",
    "noutbuk",
    "köhnə TV",
    "qayalı çuval",
    "göy qurşağı alabalığı",
    "plastik toyuq",
    "məhsul",
    "yanğın Söndürən",
    "ağır daş",
    "kir yığını",
    "arı pətəyi",
    "çürümüş ət parçası",
    "ayı",
    "ton kərpic",
]

THROW = [
    "atır",
    "fırlatır",
    "tullayır",
    "Yağır",
]

HIT = [
    "vurur",
    "Bərk vurur",
    "təpikləyir",
    "yumruqluyur",
    "keçirir",
]

# ===========================================

@register(outgoing=True, pattern="^.hayvan ?(.*)")
async def hayvan(e):
    arg = e.pattern_match.group(1)
    if arg == "pisik":
        args = "cat"
    elif arg == "it":
        args = "dog"
    elif arg == "qus":
        args = "birb"
    elif arg == "qurd":
        args = "fox"
    elif arg == "panda":
        args = "panda"
    else:
        arg = "pisik"
        args = "cat"

    foto = requests.get(f'https://some-random-api.ml/img/{args}').json()["link"]
    await e.delete()
    await e.client.send_message(
        e.chat_id,
        f"`Random bir {arg} şəkili atır`",
        file=foto
    )

@register(outgoing=True, pattern="^.qerar$")
async def karar(e):
    msaj = ""
    if e.reply_to_msg_id:
        rep = await e.get_reply_message()
        replyto = rep.id
        msaj += f"[Dosdum](tg://user?id={rep.from_id}), "
    else:
        e.edit("`Zəhmət olmasa bir mesaja cavab verin`")
        return
    yesno = requests.get('https://yesno.wtf/api').json()
    if yesno["answer"] == "yes":
        cevap = "bəli"
    else:
        cevap = "xeyr"
    msaj += f"Güman edirəm ki {cevap} deyəcəm."

    await e.delete()
    await e.client.send_message(
        e.chat_id,
        msaj,
        reply_to=replyto,
        file=yesno["image"]
    )

@register(outgoing=True, pattern=r"^.(\w+)say (.*)")
async def univsaye(cowmsg):
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern="^:/$", ignore_unsafe=True)
async def kek(keks):
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await keks.edit(":" + uio[i % 2])


@register(pattern="^.slap(?: |$)(.*)", outgoing=True)
async def who(event):
    replied_user = await get_user_from_event(event)
    if replied_user:
        replied_user = replied_user[0]
    else:
        return
    caption = await slap(replied_user, event)

    try:
        await event.edit(caption)

    except BaseException:
        await event.edit(
            "`Bu adama yumruq ata bilmirəm, yanımda çubuq və daş götürməliyəm !!`"
        )


async def slap(replied_user, event):
    user_id = replied_user.id
    first_name = replied_user.first_name
    username = replied_user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = choice(SLAP_TEMPLATES)
    item = choice(ITEMS)
    hit = choice(HIT)
    throw = choice(THROW)

    caption = "Brend " + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw)

    return caption


@register(outgoing=True, pattern="^-_-$", ignore_unsafe=True)
async def lol(lel):
    okay = "-_-"
    for i in range(10):
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@register(outgoing=True, pattern="^;_;$", ignore_unsafe=True)
async def fun(e):
    t = ";_;"
    for j in range(10):
        t = t[:-1] + "_;"
        await e.edit(t)


@register(outgoing=True, pattern="^.fp$")
async def facepalm(e):
    """ Utanmaq  🤦‍♂ """
    await e.edit("🤦‍♂")


@register(outgoing=True, pattern="^.cry$")
async def cry(e):
    """ bunu yaparsan, her zaman ağlarım !! """
    await e.edit(choice(CRI))


@register(outgoing=True, pattern="^.cp(?: |$)(.*)")
async def copypasta(cp_e):
    """ copypasta """
    textx = await cp_e.get_reply_message()
    message = cp_e.pattern_match.group(1)

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await cp_e.edit("`😂Bana💯BIR✌️mE🅱️In👐Ver👏`")
        return

    reply_text = choice(EMOJIS)
    b_char = choice(message).lower()
    for owo in message:
        if owo == " ":
            reply_text += choice(EMOJIS)
        elif owo in EMOJIS:
            reply_text += owo
            reply_text += choice(EMOJIS)
        elif owo.lower() == b_char:
            reply_text += "🅱️"
        else:
            if bool(getrandbits(1)):
                reply_text += owo.upper()
            else:
                reply_text += owo.lower()
    reply_text += choice(EMOJIS)
    await cp_e.edit(reply_text)


@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
async def vapor(vpr):
    reply_text = list()
    textx = await vpr.get_reply_message()
    message = vpr.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await vpr.edit("`Mənə 1 mətin ver!`")
        return

    for charac in message:
        if 0x21 <= ord(charac) <= 0x7F:
            reply_text.append(chr(ord(charac) + 0xFEE0))
        elif ord(charac) == 0x20:
            reply_text.append(chr(0x3000))
        else:
            reply_text.append(charac)

    await vpr.edit("".join(reply_text))


@register(outgoing=True, pattern="^.str(?: |$)(.*)")
async def stretch(stret):
    textx = await stret.get_reply_message()
    message = stret.text
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await stret.edit("`Mənə 1 mətin ver!`")
        return

    count = randint(3, 10)
    reply_text = sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                     message)
    await stret.edit(reply_text)


@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
async def zal(zgfy):
    reply_text = list()
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await zgfy.edit(
            "`Ｂ̺ͬａ̠͑ｎ̵̉ａ̬͜ ｂ̶͔ｉ̼͚ｒ͈͞ ｍ̼͘ｅ̨̝ｔ͔͙ｉ̢ͮｎ̜͗ ｖ͢͜ｅ̗͐ｒ̴ͮ`"
        )
        return

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(0, 3):
            charac += choice(ZALG_LIST[randint(0,2)]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))
    

@register(outgoing=True, pattern="^.hi$")
async def hoi(hello):
    await hello.edit(choice(HELLOSTR))


@register(outgoing=True, pattern="^.owo(?: |$)(.*)")
async def faces(owo):
    textx = await owo.get_reply_message()
    message = owo.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await owo.edit("` UwU bana bir metin ver! `")
        return

    reply_text = sub(r"(r|l)", "w", message)
    reply_text = sub(r"(R|L)", "W", reply_text)
    reply_text = sub(r"n([aeiou])", r"ny\1", reply_text)
    reply_text = sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
    reply_text = sub(r"\!+", " " + choice(UWUS), reply_text)
    reply_text = reply_text.replace("ove", "uv")
    reply_text += " " + choice(UWUS)
    await owo.edit(reply_text)


@register(outgoing=True, pattern="^.react$")
async def react_meme(react):
    await react.edit(choice(FACEREACTS))


@register(outgoing=True, pattern="^.shg$")
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    await shg.edit(choice(SHGS))


@register(outgoing=True, pattern="^.run$")
async def runner_lol(run):
    await run.edit(choice(RUNS_STR))


@register(outgoing=True, pattern="^oof$")
async def oof(e):
    t = "oof"
    for j in range(16):
        t = t[:-1] + "of"
        await e.edit(t)

                      
@register(outgoing=True, pattern="^Oof$")
async def Oof(e):
    t = "Oof"
    for j in range(16):
        t = t[:-1] + "of"
        await e.edit(t)


@register(outgoing=True, pattern="^skrrt$")
async def oof(e):
    t = "skrrt"
    for j in range(16):
        t = t[:-1] + "rt"
        await e.edit(t)
        

@register(outgoing=True, pattern="^Skrrt$")
async def oof(e):
    t = "Skrrt"
    for j in range(16):
        t = t[:-1] + "rt"
        await e.edit(t)


@register(outgoing=True, pattern="^.fuk")
async def fuk(event):
    if event.fwd_from:
        return
    animation_interval = 0.1
    animation_ttl = range(0, 101)
    animation_chars = [
            "🍆       🍑️",
            "🍆     🍑️",
            "🍆  🍑️",
            "🍆🍑️💦"
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 4])


@register(outgoing=True, pattern="^.kalp (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    deq = deque(list("️❤️🧡💛💚💙💜🖤"))
    for _ in range(32):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)
    await event.edit("❤️🧡💛" + input_str + "💚💙💜🖤")


@register(outgoing=True, pattern="^.10iq$")
async def iqless(e):
    await e.edit(
    "DÜÜT DÜÜTT AÇIQ YOLU AÇIQ HADI ŞER PARÇALARI YOLU AÇIR \n"
    "HADİ BAK Əlil GÜZƏRLƏRİ BURADA HADİ DÜÜTTT ♿️ BAK \n"
    "SINIRLI DOST HADİ HADİİ DÜÜT DÜTT BİİİPP YOLU AÇIB \n"
    "HADİ BE SÜRƏTLİ OLL DÜÜTT BİİİPPP ♿️♿️ Pişmiş sürət əlildir \n"
    "BİİİİPPP BIİİİİPPP DÜÜTTT ♿️♿️♿️♿️ BAK ARTIIO NÖMRƏLƏRİ \n"
    "BİİİİPPP BİİİİİPPP DÜÜÜTTT ♿️♿️♿️♿️ BAK ARTIYO SAYILARI \n"
    "AÇ, YOLU AÇ PÜÜÜÜ REZİLL DÜÜÜTT ♿️♿️♿️ \n"
    "♿️♿️♿️ BAXIN ÇOX DÜŞÜNÜN, DƏLİ DƏLİDİR \n"
    "AÇ YOLU DUTDUTDURURURUDUTTT♿️♿️♿️♿️♿️♿️♿️♿️♿️ \n"
    "♿️♿️♿️♿️♿️BEYİNLƏRİ YOX OLDU BUNLARIN."
    )
    
    
@register(outgoing=True, pattern="^.zarafat$")
async def mizahshow(e):
    await e.edit(
    "⚠️⚠️⚠️Zarafat Şoww😨😨😨😨😱😱😱😱😱 \n"
    "😱😱⚠️⚠️ 😂😂😂😂😂😂😂😂😂😂😂😂😂😂😱😵 \n"
    "😂😂👍👍👍👍👍👍👍👍👍👍👍👍👍 Zarafat \n"
    "Zor zarafat idi ahahahah \n"
    "AHAHAHAHAHAHHAHAHAHAHAHAHAHAHAHAHAHHAHAHAHAHA \n"
    "HAHAHAHAHAHAHHAHAHAHAHAHAHA😂😂😂😂😂😂😂😂 \n"
    "😂 ALA ÖLDÜM GÜLMƏKDƏN \n"
    "hHALALDI SƏMƏ ✔️✔️✔️✔️✔️✔️✔️✔️👏👏👏👏👏👏👏👏 \n"
    "👏 BOMBA ZARAFAT👏👏👏👏👏😂😂😂😂 \n"
    "😂😂😂😂😂😂⚠️ \n"
    "💯💯💯💯💯💯💯💯💯 \n"
    "ALA KOPYA BİZİYE 😂😂😂👏👏 \n"
    "💯💯⚠️⚠️♿️YOL POSTUNUN SAHİBİNİ VƏ MÜDAFİƏÇİLƏRİNİ AÇIN \n"
    "GƏLİR ♿️♿️ DUTT️ \n"
    "DÜÜÜÜT♿️DÜÜT♿️💯💯⚠️ \n"
    "♿️ALALAALALALALA ♿️ \n"
    "CJWJCJWJXJJWDJJQUXJAJXJAJXJWJFJWJXJAJXJWJXJWJFIWIXJQJJQJASJAXJ \n"
    "AJXJAJXJJAJXJWJFWJJFWIIFIWICIWIFIWICJAXJWJFJEICIIEICIEIFIWICJSXJJS \n"
    "CJEIVIAJXBWJCJIQICIWJX💯💯💯💯💯💯😂😂😂😂😂😂😂 \n"
    "😂⚠️😂😂😂😂😂😂⚠️⚠️⚠️😂😂😂😂♿️♿️♿️😅😅 \n"
    "😅😂👏💯⚠️👏♿️🚨"
    )    


@register(outgoing=True, pattern="^.moon$")
async def moon(event):
    deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.clock$")
async def clock(event):
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    try:
        for x in range(32):
            await sleep(0.1)
            await event.edit("".join(deq))
            deq.rotate(1)
    except BaseException:
        return


@register(outgoing=True, pattern="^.mock(?: |$)(.*)")
async def spongemocktext(mock):
    reply_text = list()
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await mock.edit("`Mənə 1 mətin ver!`")
        return

    for charac in message:
        if charac.isalpha() and randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await mock.edit("".join(reply_text))


@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
async def claptext(memereview):
    textx = await memereview.get_reply_message()
    message = memereview.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await memereview.edit("`Hah, mənasızdı amma təbrik edirəm!`")
        return
    reply_text = "👏 "
    reply_text += message.replace(" ", " 👏 ")
    reply_text += " 👏"
    await memereview.edit(reply_text)


@register(outgoing=True, pattern=r"^.f (.*)")
async def payf(event):
    paytext = event.pattern_match.group(1)
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2)
    await event.edit(pay)

@register(outgoing=True, pattern=r"^.ğ (.*)")
async def payg(event):
    g = """
     ㅤ 
          ❤️❤️❤️❤️❤️❤️

          ❤️❤️❤️❤️❤️❤️
     ❤️❤️❤️❤️❤️❤️❤️❤️
   ❤️❤️                     ❤️❤️
 ❤️❤️
❤️❤️                ❤️❤️❤️❤️
❤️❤️                ❤️❤️❤️❤️
 ❤️❤️                        ❤️❤️
   ❤️❤️                      ❤️❤️
     ❤️❤️❤️❤️❤️❤️❤️❤️
          ❤️❤️❤️❤️❤️❤️
"""
    paytext = event.pattern_match.group(1)
    await event.edit(g.replace('❤️', paytext))

@register(outgoing=True, pattern=r"^.bo[sş]luk")
async def bosluk(event):
    await event.delete()
    await event.reply('ㅤ')

@register(outgoing=True, pattern="^.lfy (.*)")
async def let_me_google_that_for_you(lmgtfy_q):
    textx = await lmgtfy_q.get_reply_message()
    qry = lmgtfy_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
    payload = {'format': 'json', 'url': lfy_url}
    r = requests.get('http://is.gd/create.php', params=payload)
    await lmgtfy_q.edit(f"İşte, keyfine bak.\
    \n[{query}]({r.json()['shorturl']})")


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
async def scam(event):
    options = [
        'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
        'photo', 'document', 'cancel'
    ]
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(30, 60)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(30, 60)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await event.edit("`Invalid Syntax !!`")
        return
    try:
        if (scam_time > 0):
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("`Mənə 1 mətin ver!`")
        return
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)

CmdHelp('memes').add_command(
    'hayvan', 'Pişik/it/panda/quş/qurd', 'Random heyvan fotosu atır.'
).add_command(
    'cowsay', None, 'Nəsə deyən inək)'
).add_command(
    ':/', None, 'Animasiyon.'
).add_command(
    'qerar', None, 'Qərar verin.'
).add_command(
    '-_-', None, 'Anladım.'
).add_command(
    ';_;', None, '5 dəqiqə sevgilini görmədən fikirləş.'
).add_command(
    'cp', '<yanıt>', 'Emoji falan əlavə edir.'
).add_command(
    'vapor', '<mesaj/yanıtlama>', 'Vaporlaştırın!'
).add_command(
    'str', '<yazı>', 'Yazıyı uzad.'
).add_command(
    '10iq', None, 'Selax mesaj yazır.'
).add_command(
    'zarafat', None, 'Animasiyon'
).add_command(
    'zal', '<yanıtlama/mesaj>', 'Çox mürəkkəb! Hər şey çox mürəkkəbdir.'
).add_command(
    'oof', None, 'yaxşıda bildim'
).add_command(
    'skrrt', None, 'sıkırt'
).add_command(
    'fuk', None, '+18'
).add_command(
    'kalp', '<ad>', 'Sevginizi göstərin.'
).add_command(
    'fp', None, 'Utanmaq.'
).add_command(
    'moon', None, 'Ay animasiyası.'
).add_command(
    'clock', None, 'Saat animasyonu'
).add_command(
    'hi', None, 'Salam verin.'
).add_command(
    'owo', None, 'Lolist Selin kimi'
).add_command(
    'react', None, 'Ayzırbotu hər şeyə reaksiya verin.'
).add_command(
    'slap', '<yanıtlama>', 'Təsadüfi obyektlərlə sürüşdürmək üçün mesajı cavablandırın.'
).add_command(
    'cry', None, 'Ağlamaq istəyirsən?'
).add_command(
    'shg', None, '¯\_(ツ)_/¯'
).add_command(
    'run', None, 'Koş!'
).add_command(
    'mock', '<yanıtlama/mesaj>', 'Bunu et və həqiqi əyləncəni tap.'
).add_command(
    'clap', None, 'Animasiya!'
).add_command(
    'f', '<mesaj>', 'F'
).add_command(
    'type', '<yazı>', 'Daktilo Kimi mətn yazın.'
).add_command(
    'lfy', '<sual>', 'Google-un sizin üçün bunu axtarmasına icazə verin.'
).add_command(
    'scam', '<hərəkət> <vaxt>', 'Saxta hərəkətlər yaradın.\nCari yərəkətlər: (typing, contact, game, location, voice, round, video, photo, document, cancel)'
).add_command(
    'lfy', '<sual>', 'Google-un sizin üçün bunu axtarmasına icazə verin.'
).add_command(
    'boşluk', None, 'Boş mesaj.'
).add_command(
    'ğ', '<metin>', 'Ğ'
).add()
