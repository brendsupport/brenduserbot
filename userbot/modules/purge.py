from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("purge")

@register(outgoing=True, pattern="^.temizle$")
async def fastpurger(purg):

    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit(LANG['NEED_MSG'])
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id, LANG['PURGED'].format(str(count)))

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "Hədəflənən " + str(count) + " mesaj müvəffəqiyyətlə silindi.")
    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern="^.mesajimisil")
async def purgeme(delme):
    
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id,
                                                    from_user='me'):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        LANG['PURGED_ME'].format(str(count))
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "Hədəflənən " + str(count) + " mesaj müvəffəqiyyətlə silindi.")
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern="^.sil$")
async def delete_it(delme):

    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Hədəflənən mesajın silinməsi müvəffəqiyyətlə tamamlandı")
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Bu mesajı silə bilmirəm.")


@register(outgoing=True, pattern="^.d[uü]z{eə]lt")
async def editer(edit):

    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id('me')
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(BOTLOG_CHATID,
                                       "Mesaj düzəltmə müvəffəqiyyətlə tamamlandı")


@register(outgoing=True, pattern="^.gizli")
async def selfdestruct(destroy):

    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    if BOTLOG:
        await destroy.client.send_message(BOTLOG_CHATID,
                                          "gizli sorğusu uğurla başa çatıb")

CmdHelp('purge').add_command(
    'temizle', None, 'Hedeflenen yanıttan başlayarak tüm mesajları temizler.'
).add_command(
    'mesajimisil', 'Hədəflənən mesajdan başlayaraq öz mesajlarınızı silər.'
).add_command(
    'sil', '<cavab>', 'Göstərdiyiniz mesajı silir.'
).add_command(
    'duzelt və ya düzəlt', '<yeni mesaj>', 'Cavab verdiyiniz mesajı yeni mesaj ile dəyişdirir.'
).add_command(
    'gizli', '<saniyə> <mesaj>', 'x saniye içində özünü yox edən bir mrsaj düzəldər.'
).add()
