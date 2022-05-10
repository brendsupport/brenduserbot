# ᴇʟçɪɴ ⥌ 🇯🇵

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp


@register(outgoing=True, pattern="^.tt(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("`Mənə yükləməyim üçün bir link ver..`")
    else:
        await event.edit("`BrendUserBot tərəfindən yüklənir⚡️...`")
    chat = "@ttsavebot"
    async with event.client.conversation(chat) as conv:
        try:
            msg_start = await conv.send_message("/start")
            r = await conv.get_response()
            msg = await conv.send_message(d_link)
            details = await conv.get_response()
            video = await conv.get_response()
            """ - don't spam notif - """
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.edit("`Xahiş edirəm` @ttsavebot `blokdan çıxarıb yenidən yoxlayın`")
            return
        await event.client.send_file(event.chat_id, video ,caption=f"[ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ⚡️](t.me/BrendUserBot)`ilə yükləndi`")
        await event.client.delete_messages(conv.chat_id,
                                           [msg_start.id, r.id, msg.id, details.id, video.id])
        await event.delete()

@register(outgoing=True, pattern="^.ig ?(.*)")
async def insta(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir linkə cavab ver`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("`Düzgün bir link ver`")
        return
    chat = "@SaveAsBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("`Yükləməyim üçün instagram linkinə ehtiyacım var..`")
        return
    await event.edit('`BrendUserBot tərəfindən yüklənir⚡️`')
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=523131145)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("`Xahiş olunur @SaveAsBot`u blokdan çıxarıb yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "Media gizli hesabdır."
            )
        else:
            await event.delete()
            await event.client.send_file(event.chat_id,response.message.media,caption=f"[ʙʀᴇɴᴅ ᴜꜱᴇʀʙᴏᴛ⚡️](t.me/BrendUserBot)`ilə yükləndi`")
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.delete()


CmdHelp('saver').add_command(
    'tt', '<link>', 'Tiktokdan media yükləyər..'
).add_command(
    'ig', '<linkə cavab olaraq>', 'İnstagramdan video yükləyər.'
).add()




       
