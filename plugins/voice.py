import asyncio
import os
from pyrogram.raw import types
from gtts import gTTS
from pyrogram import filters,Client


lang = "en"  # Default Language for voice


@Client.on_message(filters.command("voice"))
async def voice(client, message):
    global lang
    cmd = message.command
    if len(cmd) > 1:
        v_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        v_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`――――――――――――[ERROR]―――――――――――\nSir, reply to a message or send text arg to convert to voice\n―――――――――――――――――――――――――――――`")
        await asyncio.sleep(2)
        await message.delete()
    # noinspection PyUnboundLocalVariable
    tts = gTTS(v_text, lang=lang)
    tts.save(f'{v_text}.mp3')
    await message.delete()
    if message.reply_to_message:
        await client.send_voice(message.chat.id, voice=f'{v_text}.mp3',reply_to_message_id=message.reply_to_message.id)
    else:
        await client.send_voice(message.chat.id, voice=f'{v_text}.mp3')
    os.remove(f'{v_text}.mp3')


@Client.on_message(filters.command("voicelang"))
async def voicelang(client, message):
    global lang
    temp = lang
    lang = message.text.split(None, 1)[1]
    try:
        gTTS("tes", lang=lang)
    except Exception as e:
        await message.reply("Wrong Language id !")
        lang = temp
        return
    await message.reply("Language Set to {}".format(lang))

@Client.on_message(filters.command("promote"))
async def promote_usr(client, message):
    peer = await client.resolve_peer("paura")
    if isinstance(peer, types.InputPeerUser):
        user_id = int(peer.user_id)
    await client.promote_chat_member(message.chat.id, user_id)




