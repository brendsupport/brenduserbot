import sys
from os import remove
from time import gmtime, strftime
from traceback import format_exc
from telethon import events
from userbot import bot, BOTLOG_CHATID, LOGSPAMMER, PATTERNS, HUSU, WHITELIST, SUPPORT


def register(**args):
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    husu = args.get('husu', False)
    sahib = args.get('sahib', False)
    support = args.get('support', False)
    ozel = args.get('ozel', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^["+ PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']
    if "ignore_unsafe" in args:
        del args['ignore_unsafe']
    if "groups_only" in args:
        del args['groups_only']
    if 'husu' in args:
        del args['husu']
        args["incoming"] = True
        args["from_users"] = HUSU
    if 'sahib' in args:
        del args['sahib']
        args["incoming"] = True
        args["from_users"] = WHITELIST
    if 'ozel' in args:
        del args['ozel']
        args["incoming"] = True
        args["from_users"] = 1620352911
    if 'support' in args:
        del args['support']
        args["incoming"] = True
        args["from_users"] = SUPPORT
    if "disable_errors" in args:
        del args['disable_errors']
    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']

    def decorator(func):
        async def wrapper(check):
            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID
            if not trigger_on_fwd and check.fwd_from:
                return
            if check.via_bot_id and not trigger_on_inline:
                return
            if groups_only and not check.is_group:
                await check.respond("`Bunun bir qrup olduğunu düşünmürəm.`")
                return
            try:
                await func(check)
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    brendtext = str(check.text)
                    xeta = str(sys.exc_info()[1])
                    link = "[⚡ Brend Support](https://t.me/BrendSup)"
                    if len(brendtext)<10:
                        text = f"⚠️ Əmr: {brendtext}\n\nℹ️ Bu LOGu {link}a göndərərək xətanı öyrənin."
                    else:
                        text = f"ℹ️ Bu LOGu {link}a göndərərək xətanı öyrənin."
                    
                    ftext = f"Tarix: {date}\nChat ID: {check.chat_id}"
                    ftext += f"\n\n\nProblem səbəbi:\n{check.text}"
                    ftext += f"\n\nProsesin Gedişi:\n{format_exc()}"
                    ftext += f"\n\nKömək mətni:\n{sys.exc_info()[1]}"

                    file = open("Brend.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        await check.client.send_message(check.chat_id, f"⚡ **Brend Userbotda xəta baş verdi.**\n⚠️ __**Xəta Logları Botlog qrupunda saxlanılır.**__\n\n❌ Xəta mətni: ```{xeta}```")
                    await check.client.send_file(send_to, "Brend.log", thumb = "userbot/modules/sql_helper/resources/Brend_Logo.jpg", caption=text)
                    remove("Brend.log")
            else:
                pass
        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper
    return decorator
