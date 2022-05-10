from pydub import AudioSegment
from json import dumps
from userbot.events import register
from .shazam_helper.communication import recognize_song_from_signature
from .shazam_helper.algorithm import SignatureGenerator
from requests import get
from os import remove
import urllib.parse
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.shazam")
async def shazam(event):
    if not event.is_reply:
        return await event.edit('`Xahiş olunur bir səs faylına cavab verin!`')
    else:
        await event.edit('`Səs faylı yüklənir...`')
        reply_message = await event.get_reply_message()
        dosya = await reply_message.download_media()

        await event.edit('`Səs faylı brend formatına çevrilir...`')
        audio = AudioSegment.from_file(dosya)
        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_channels(1)
            
        signature_generator = SignatureGenerator()
        signature_generator.feed_input(audio.get_array_of_samples())
            
        signature_generator.MAX_TIME_SECONDS = 12
        if audio.duration_seconds > 12 * 3:
            signature_generator.samples_processed += 16000 * (int(audio.duration_seconds / 2) - 6)
            
        results = '{"error": "Not found"}'
        sarki = None
        await event.edit('` Shazamlanır...`')
        while True:
            signature = signature_generator.get_next_signature()
            if not signature:
                sarki = results
                break
            results = recognize_song_from_signature(signature)
            if results['matches']:
                sarki = results
                break
            else:
                await event.edit(f'`İlk {(signature_generator.samples_processed / 16000)} saniyədə heç bir şey tapılmadı... yenidən yoxlayıram.`')
        
        if not 'track' in sarki:
            return await event.edit('`Təssüf ki Shazam bu səsi tapa bilmədi. Biraz daha aydın səs atın`')
        await event.edit('`Mahnını tapdım... Məlumatları tapdım...`')
        Caption = f'**Mahnı:** [{sarki["track"]["title"]}]({sarki["track"]["url"]})\n'
        if 'artists' in sarki['track']:
            Caption += f'**Oxuyan(lar):** [{sarki["track"]["subtitle"]}](https://www.shazam.com/artist/{sarki["track"]["artists"][0]["id"]})\n'
        else:
            Caption += f'**Oxuyan(lar):** `{sarki["track"]["subtitle"]}`\n'

        if 'genres'in sarki['track']:
            Caption += f'**Janr:** `{sarki["track"]["genres"]["primary"]}`\n'

        if sarki["track"]["sections"][0]["type"] == "SONG":
            for metadata in sarki["track"]["sections"][0]["metadata"]:
                Caption += f'**{"İl" if metadata["title"] == "Sorti" else metadata["title"]}:** `{metadata["text"]}`\n'

        Caption += '\n**Musiqi platformaları:** '
        for provider in sarki['track']['hub']['providers']:
            if provider['actions'][0]['uri'].startswith('spotify:track'):
                Url = provider['actions'][0]['uri'].replace(
                    'spotify:track:', 'http://open.spotify.com/track/'
                )
            elif provider['actions'][0]['uri'].startswith('intent:#Intent;action=android.media.action.MEDIA_PLAY_FROM_SEARCH'):
                Url = f'https://open.spotify.com/search/' + urllib.parse.quote(sarki["track"]["subtitle"] + ' - ' + sarki["track"]["title"])
            elif provider['actions'][0]['uri'].startswith('deezer'):
                Url = provider['actions'][0]['uri'].replace(
                    'deezer-query://', 'https://'
                )
            else:
                Url = provider['actions'][0]['uri']
            Caption += f'[{provider["type"].capitalize()}]({Url}) '
        for section in sarki['track']['sections']:
            if section['type'] == 'VIDEO':
                if 'youtubeurl' in section:
                    Youtube = get(section['youtubeurl']).json()
                else:
                    return

                Caption += f'\n**Mahnının Videosu:** [Youtube]({Youtube["actions"][0]["uri"]})'

        if 'images' in sarki["track"] and len(sarki["track"]["images"]) >= 1:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                sarki["track"]["images"]["coverarthq"] if 'coverarthq' in sarki["track"]["images"] else sarki["track"]["images"]["background"],
                caption=Caption,
                reply_to=reply_message
                )
        else:
            await event.edit(Caption)  
        remove(dosya)

CmdHelp('shazam').add_command(
    'shazam', '<cavab>', 'Cavab verdiyiniz  səs faylını Shazamda axtarar.'
).add()
