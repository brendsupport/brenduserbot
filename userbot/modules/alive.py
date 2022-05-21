# Copyright Brend Userbot
# Created t.me/BrendOwner

from userbot.main import PLUGIN_MESAJLAR
from userbot.events import register
from telethon import version
from platform import python_version
from userbot.cmdhelp import CmdHelp
from userbot import CMD_HELP, ALIVE_NAME, BREND_VERSION, bot, SAHIB, WHITELIST
from userbot.language import get_value
LANG = get_value("alives")


@register(outgoing=True, pattern="^.alive$")
async def alive(e):
    me = await e.client.get_me()
    if type(PLUGIN_MESAJLAR['alive']) == str:
        await e.edit(PLUGIN_MESAJLAR['alive'].format(
            telethon=version.__version__,
            python=python_version(),
            brend=BREND_VERSION,
            plugin=len(CMD_HELP),
            id=me.id,
            username='@' + me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
            first_name=me.first_name,
            last_name=me.last_name if me.last_name else '',
            mention=f'[{me.first_name}](tg://user?id={me.id})'
        ))
    else:
        await e.delete()
        if not PLUGIN_MESAJLAR['alive'].text == '':
            PLUGIN_MESAJLAR['alive'].text = PLUGIN_MESAJLAR['alives'].text.format(
                telethon=version.__version__,
                python=python_version(),
                brend=BREND_VERSION,
                plugin=len(CMD_HELP),
                id=me.id,
                username='@' + me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
                first_name=me.first_name,
                last_name=me.last_name if me.last_name else '',
                mention=f'[{me.first_name}](tg://user?id={me.id})'
            )
        if e.is_reply:
            await e.respond(PLUGIN_MESAJLAR['alive'], reply_to=e.message.reply_to_msg_id)
        else:
            await e.respond(PLUGIN_MESAJLAR['alive'])


@register(outgoing=True, disable_errors=True, pattern="^.alives$")
async def brendalives(alive):
    img = PLUGIN_MESAJLAR['alives']
    caption = (
            "╭✠╼━━━━━━❖━━━━━━━✠╮\n"
            f"┣[• {LANG['ALIVE1']}󠀁󠀁󠀁󠀁󠀁󠀁󠀁󠀁󠀁󠀁\n"
            f"┣[• {LANG['ALIVE2']} {ALIVE_NAME}\n"
            f"┣[• {LANG['ALIVE3']} {len(CMD_HELP)}\n"
            "┣✠╼━━━━━━❖━━━━━━━✠\n"
            f"┣[• {LANG['ALIVE4']} {python_version()}\n"
            f"┣[• {LANG['ALIVE5']} {version.__version__}\n"
            f"┣[• {LANG['ALIVE6']} {BREND_VERSION}\n"
            "╰✠╼━━━━━━❖━━━━━━━✠╯")
    await bot.send_file(alive.chat_id, img, caption=caption)
    await alive.delete()

@register(support=True, pattern="^.balive$")
async def balive(balive):
    if balive.is_reply:
        cavab = await balive.get_reply_message()
        brend = await balive.client.get_entity(cavab.from_id)
        if brend.id == SAHIB:
            if SAHIB not in WHITELIST:
                await balive.reply(LANG['ALIVE7'].format(ALIVE_NAME, BREND_VERSION))

@register(sahib=True, pattern="^.calive(?: |$)(.*)")
async def dbalive(e):
  sebeb = e.pattern_match.group(1)
  await e.reply(f"{sebeb}")           
           
@register(sahib=True, pattern="^.dalive$")
async def dalive(dalive):
  await dalive.reply("`ﾒ 𝙱𝚛彡𝚗𝚍 hər yerdə⚡️...`")                          

@register(husu=True, pattern=f"{ALIVE_NAME}$")
async def husuaktivlesdirdi(event):
  if SAHIB not in WHITELIST:
    await event.reply(f"**⚡ Salam Hüsü mənim qurulumum sona çatdı köməkliyin üçün təşəkkürlər mənim sahibimdə artıq BRENDdi 😎**")

CmdHelp('alive').add_command('alive', None, 'Userbotun Aktivliyini yoxlamaq üçün.').add_command('alives', None, 'Medialı aktivlik yoxlanması.').add()
