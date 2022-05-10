# 𝚎𝚕𝚌𝚓𝚗  🎴⚡️

import os
from telethon import events
from sqlalchemy.exc import IntegrityError
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot import BREND_VERSION
from userbot import BREND_MENTION


from telethon.errors.rpcerrorlist import YouBlockedUserError


bot = "@MissRose_bot"


@register(outgoing=True, pattern=r"^\.fstat(?: |$)(.*)")
async def j(brend):
    await brend.edit("`Brend userbot tərəfindən yoxlanır⚡️..`")
    if brend.reply_to_msg_id:
        previous_message = await brend.get_reply_message()
        sysarg = str(previous_message.sender_id)
        user = f"[user](tg://user?id={sysarg})"
        if brend.pattern_match.group(1):
            sysarg += f" {brend.pattern_match.group(1)}"
    else:
        sysarg = brend.pattern_match.group(1)
        user = sysarg
    if sysarg == "":
        await brend.edit(
            "`Fstat etməyim üçün mənə bir id, username ver , və ya yoxlamaq istədiyiniz istifadəçiyə cavab ver`",
        )
        return
    else:
        async with brend.client.conversation(bot) as conv:
            try:
                await conv.send_message("/start")
                await conv.get_response()
                await conv.send_message("/fedstat " + sysarg)
                audio = await conv.get_response()
                if audio.message.startswith("This command can only be used once"):
                    return await brend.edit(
                        "**Bu əmr 1 dəqiqədən bir işlədilə bilər**",
                    )
                elif "Looks like" in audio.text:
                    await audio.click(0)
                    await asyncio.sleep(2)
                    audio = await conv.get_response()
                    await brend.client.send_file(
                        brend.chat_id,
                        audio,
                        caption=f"Istifadəçi: {user}\n\nPowerd by @BrendUserBot⚡️ .",
                        link_preview=False,
                    )
                    await brend.delete()
                else:
                    lcjn = await conv.get_edit()
                    await brend.edit(lcjn.message)
                await brend.client.send_read_acknowledge(bot)
            except YouBlockedUserError:
                await brend.edit("**XƏTA**\n  @MissRose_Bot `blokdan çıxar`")

                
@register(outgoing=True, pattern=r"^\.fedinfo(?: |$)(.*)")
async def _(event):
    sysarg = event.pattern_match.group(1).strip()
    async with event.client.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + sysarg)
            audio = await conv.get_response()
            await event.client.send_read_acknowledge(bot)
            await event.edit(audio.text + "\n\n**FedInfo BrendUserBot tərəfindən hazırlandı⚡️**")
        except YouBlockedUserError:
            await event.edit("**Error**\n @MissRose_Bot `blokun açıb yenidən yoxla")


@register(outgoing=True, pattern=r"^\.myfeds(?: |$)(.*)")
async def _(event):
    sysarg = event.pattern_match.group(1).strip()
    async with event.client.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/myfeds " + sysarg)
            audio = await conv.get_response()
            await event.client.send_read_acknowledge(bot)
            await event.edit(audio.text + "\n\n**FedInfo BrendUserBot tərəfindən hazırlandı⚡️**")
        except YouBlockedUserError:
            await event.edit("**Error**\n @MissRose_Bot `blokun açıb yenidən yoxla")


@register(outgoing=True, pattern=r"^\.fban(?: |$)(.*)")
async def _(event):
    sysarg = event.pattern_match.group(1).strip()
    async with event.client.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fban " + sysarg)
            audio = await conv.get_response()
            await event.client.send_read_acknowledge(bot)
            await event.edit(audio.text + "\n\n**⚡️ 𝙱𝚛彡𝚗𝚍  𝚄𝚜𝚎𝚛𝙱𝚘𝚝 fban verdi**")
        except YouBlockedUserError:
            await event.edit("**Error**\n @MissRose_Bot `blokun açıb yenidən yoxla")


@register(outgoing=True, pattern=r"^\.funban(?: |$)(.*)")
@register(outgoing=True, pattern=r"^\.unfban(?: |$)(.*)")
async def _(event):
    sysarg = event.pattern_match.group(1).strip()
    async with event.client.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/unfban " + sysarg)
            audio = await conv.get_response()
            await event.client.send_read_acknowledge(bot)
            await event.edit(audio.text + "\n\n**⚡️ 𝙱𝚛彡𝚗𝚍  𝚄𝚜𝚎𝚛𝙱𝚘𝚝 fbanı açdı**")
        except YouBlockedUserError:
            await event.edit("**Error**\n @MissRose_Bot `blokun açıb yenidən yoxla")


CmdHelp('rose').add_command(
    'fstat', '<istifadəçi adı, id və ya cavablama >', 'Göstərilən istifadəçinin hansı federasiyalarda qadağan olduğunu yoxlayın.'
).add_command(
    'fedinfo', '<fed id>', 'Federasiyalar haqqında məlumat alın.'
).add_command(
    'myfeds', None , 'Hansı fedlərdə admin olduğunuza baxın'
).add_command(
    'fban', '<istifadəçi adı, id>', 'Sahib olduğunuz feddən fban verər'
).add_command(
    'unfban', '<istifadəçi adı, id>', 'verilən fbanı sahib olduğunuz feddə açar'
).add()
