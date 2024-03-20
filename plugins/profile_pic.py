from pyrogram import Client,filters
import os

# Initialize a group call factory
@Client.on_message(filters.command("profile"))
async def d_jokes(client, message):
 user = message.from_user
 user = await client.get_chat(user.id)
 await client.download_media(user.photo.small_file_id,file_name=f"{user.username}.jpg")
 await client.send_photo(message.chat.id,f"downloads/{user.username}.jpg", caption=f"**Username**: {user.username}\n**UserID**: {user.id} ")
 os.remove(f"downloads/{user.username}.jpg")
