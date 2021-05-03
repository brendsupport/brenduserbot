import os
from requests import post
from userbot import bot, OCR_SPACE_API_KEY, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp

from userbot.language import get_value
LANG = get_value("ocr")

async def ocr_space_file(filename,
                         overlay=False,
                         api_key=OCR_SPACE_API_KEY,
                         language='tur'):
    """ OCR.space API yerli fayl tələb edir.
        Python3.5 və yuxarı üçün - 2.7-də sınaqdan keçirilməyib.
    :param filename: Fayl yolu və adı.
    :param overlay: Cavabınızda OCR.space yerləşdirilməsi tələb olunur?
                    Varsayılan olaraq yox.
    :param api_key: OCR.space API key.
                    varsayılan olarak 'salamdünya'.
    :param language: OCR'de istifadə ediləcək dil kodu.
                    Mövcud dil kodlarının siyahısını burada tapa bilərsiniz. https://ocr.space/OCRAPI
                    Varsayılan olaraq 'az'.
    :return: Nəticələr JSON formatında gəlir.
    """

    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@register(pattern=r".ocr (.*)", outgoing=True)
async def ocr(event):
    await event.edit(LANG['READING'])
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY)
    test_file = await ocr_space_file(filename=downloaded_file_name,
                                     language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await event.edit(LANG['CANT_READ'])
    else:
        await event.edit(f"`{LANG['READ']}`\n\n{ParsedText}"
                         )
    os.remove(downloaded_file_name)

CmdHelp('ocr').add_command(
    'ocr', '<dil>', 'Mətn çıxarmaq üçün şəkilə və ya stikerə cavab verin.'
).add_info(
    'Dil kodlarını [burdan](https://ocr.space/ocrapi) tapa bilərsiniz.'
).add()
