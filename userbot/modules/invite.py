# Modul Brend Userbot'a aiddir
# Oğurlama atanın balası

from telethon.tl import functions
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.errors import ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError
from telethon.tl.functions.channels import GetFullChannelRequest
from userbot.modules.admin import *
from userbot.events import register
from userbot.cmdhelp import CmdHelp


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    yoxla = ["@BrendSUP", "@BrendSupport", "@BrendSohbet", "t.me/BrendSUP", "t.me/BrendSupport", "t.me/BrendSohbet", "@brendsup", "@brendsupport", "t.me/brendsup", "t.me/brendsupport"]
    if chat in yoxla:
        await event.reply(f"Mən {chat} qrupunu əsla daşıya bilmərəm!", link_preview=False)
        await event.client.send_message(-1001197418406, "Mənim sahibim bu qrupu daşımağa çalışır @admins.")
        return
    else:
        chat_info = None
        if chat:
            try:
                chat = int(chat)
            except ValueError:
                pass
        if not chat:
            if event.reply_to_msg_id:
                replied_msg = await event.get_reply_message()
                if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                    chat = replied_msg.fwd_from.channel_id
            else:
                chat = event.chat_id
        try:
            chat_info = await event.client(GetFullChatRequest(chat))
        except BaseException:
            try:
                chat_info = await event.client(GetFullChannelRequest(chat))
            except ChannelInvalidError:
                await event.reply("`Xətalı qrup`")
                return None
            except ChannelPrivateError:
                await event.reply("`Bu qrup gizlidir və ya banlanmısan`")
                return None
            except ChannelPublicGroupNaError:
                await event.reply("`Qrup mövcud deyil`")
                return None
            except (TypeError, ValueError):
                await event.reply("`Xətalı qrup`")
                return None
        return chat_info


@register(outgoing=True, groups_only=True, disable_errors=True, pattern=r"^\.invite(?: |$)(.*)")
async def brendinvite(event):
    await event.edit("`Başladılır...`")
    brendteam = await get_chatinfo(event)
    chat = await event.get_chat()
    if event.is_private:
        return await event.edit("`Təssüf ki bura üzv əlavə edilə bilmir`")
    s = 0
    f = 0
    error = 'None'
    await event.edit("**Hazır ki vəziyyət**\n\n`İstifadəçilər dəvət edilir.......`")
    async for user in event.client.iter_participants(brendteam.full_chat.id):
        try:
            if error.startswith("Too"):
                return await event.edit(f"**Dəvət uğursuzluqla nəticələndi**\n(`məhdudlaşma xətası ola bilər Xahiş edirəm daha sonra yenidən cəhd edin `)\n**XƏTA❌** : \n`{error}`\n\n• dəvət edildi `{s}`  \n• Uğursuz dəvətlər: `{f}`")
            await event.client(functions.channels.InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1
            await event.edit(f"**Dəvət edilir...**\n\n• Əlavə olundu `{s}` \n• Uğursuz dəvətlər `{f}` \n\n**× LastError:** `{error}`")
        except Exception as e:
            error = str(e)
            f = f + 1
    return await event.edit(f"**Dəvət Yekunlaşdı** \n\n• Uğurla nəticələnən dəvətlər `{s}` \n• Uğursuz Dəvətlər `{f}` ")
@register(outgoing=True, pattern="^.add ?(.*)")
@register(outgoing=True, pattern="^.[eə]lav[eə] ?(.*)")
async def elave(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("Bu əmr şəxsi söhbət bölümü üçün nəzərdə tutlmayıb!")
    else:
        if not event.is_channel and event.is_group:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} qrupa əlavə edilir...`')
                try:
                    await event.client(AddChatUserRequest(chat_id=event.chat_id, user_id=user_id, fwd_limit=1000000))
                except Exception as e:
                    await event.edit(f'`{user_id} qrupa əlavə edə bilmədim!`')
                    continue
                await event.edit(f'`{user_id} qrupa əlavə elədim!`')
        else:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} qrupa əlavə olunur...`')
                try:
                    await event.client(InviteToChannelRequest(channel=event.chat_id, users=[user_id]))
                except Exception as e:
                    await event.edit(f'`{user_id} qrupa əlavə oluna bilmədi!`')
                    continue
                await event.edit(f'`{user_id} qrupa əlavə olundu!`')

CmdHelp('invite').add_command(
    'invite', '<Qrup linki>', 'Linkini yazdığınız qrupdan adam daşımaq.'
).add_command(
    'add', '<istifadəçi adı>', 'Bir İstifadəçini Qrupa əlavə edər'
).add()
