# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from asyncio import sleep
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("notes")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.notes$")
async def notes_active(svd):
    try:
        from userbot.modules.sql_helper.notes_sql import get_notes
    except AttributeError:
        await svd.edit("`Bot qeyri-SQL rejimində işləyir!!`")
        return
    message = LANG['NOT_FOUND']
    notes = get_notes(svd.chat_id)
    for note in notes:
        if message == LANG['NOT_FOUND']:
            message = f"{LANG['NOTES']}:\n"
            message += "`#{}`\n".format(note.keyword)
        else:
            message += "`#{}`\n".format(note.keyword)
    await svd.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(clr):
    try:
        from userbot.modules.sql_helper.notes_sql import rm_note
    except AttributeError:
        await clr.edit("`Bot qeyri-SQL rejimində işləyir!!`")
        return
    notename = clr.pattern_match.group(1)
    if rm_note(clr.chat_id, notename) is False:
        return await clr.edit(" **{}** `{}`".format(notename, LANG['CLEAR_NOT_FOUND']))
    else:
        return await clr.edit(
            "**{}** `{}`".format(notename, LANG['CLEAR']))


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_note(fltr):
    try:
        from userbot.modules.sql_helper.notes_sql import add_note
    except AttributeError:
        await fltr.edit("`Bot qeyri-SQL rejimində işləyir!!`")
        return
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await fltr.client.send_message(
                BOTLOG_CHATID, f"#NOTE\
            \nGrup ID: {fltr.chat_id}\
            \nAçar söz: {keyword}\
            \n\nÇatdakı qeydə cavab vermək üçün bu mesaj qeyd edildi, xahiş edirəm bu mesajı silməyin!"
            )
            msg_o = await fltr.client.forward_messages(entity=BOTLOG_CHATID,
                                                       messages=msg,
                                                       from_peer=fltr.chat_id,
                                                       silent=True)
            msg_id = msg_o.id
        else:
            await fltr.edit(
                "`Medianı qeyd kimi saxlamaq üçün BOTLOG_CHATID dəyəri təyin olunmalıdır.`"
            )
            return
    elif fltr.reply_to_msg_id and not string:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
    success = "`{} {}. ` #{} `{}`"
    if add_note(str(fltr.chat_id), keyword, string, msg_id) is False:
        return await fltr.edit(success.format(LANG['SUCCESS'], 'güncəllendi', keyword, LANG['CALL']))
    else:
        return await fltr.edit(success.format(LANG['SUCCESS'], 'Əlavə edildi', keyword, LANG['CALL']))


@register(pattern=r"#\w*",
          disable_edited=True,
          disable_errors=True,
          ignore_unsafe=True)
async def incom_note(getnt):
    try:
        if not (await getnt.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.notes_sql import get_note
            except AttributeError:
                return
            notename = getnt.text[1:]
            note = get_note(getnt.chat_id, notename)
            message_id_to_reply = getnt.message.reply_to_msg_id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note and note.f_mesg_id:
                msg_o = await getnt.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(
                                                            note.f_mesg_id))
                await getnt.client.send_message(getnt.chat_id,
                                                msg_o.mesage,
                                                reply_to=message_id_to_reply,
                                                file=msg_o.media)
            elif note and note.reply:
                await getnt.client.send_message(getnt.chat_id,
                                                note.reply,
                                                reply_to=message_id_to_reply)
    except AttributeError:
        pass

CmdHelp('notes').add_command(
    '#<notismi>', None, 'Göstərilən qeydi çağırır.'
).add_command(
    'save', '<qeyd adı> <qeyd ediləcək bir şey> ya da mesajı .save <not adı> cavab verərək istifadə olunur', 'Cavab verilmiş mesajı adı ilə qeyd şəklində saxlayır. (Həm də şəkillər, sənədlər və stikerlər üzərində işləyir.)'
).add_command(
    'notes', None, 'Söhbətdəki bütün qeydləri xatırladır.'
).add_command(
    'clear', '<qeyd adı>', 'Göstərilən qeyd silinir.'
).add()
