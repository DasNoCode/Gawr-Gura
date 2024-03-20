import tracemoepy
from pyrogram import Client, filters
import os

tracemoe = tracemoepy.tracemoe.TraceMoe()


@Client.on_message(filters.command('whatanime'))
async def whatanime(_, message):
    reply = message.reply_to_message
    if reply and reply.media:
        path = reply.download()
        info = tracemoe.search(path, upload_file=True)
        data = f"Match: {info.result[0].anilist.title.romaji}\nSimilarity: {info.result[0].similarity*100}"
        info.result[0].save(f"{reply.from_user.id}.mp4", mute=False)
        reply.reply_document(f"{reply.from_user.id}.mp4", caption=data)
        os.remove(f"{reply.from_user.id}.mp4")


