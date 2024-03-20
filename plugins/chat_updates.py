from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import pymongo 
from decouple import config

MONGO_URL = config("MONGO_URL", default=None)
mongo = pymongo.MongoClient(MONGO_URL)
db_name = "chatservices"

async def admin_check(message) -> bool:
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    if check_status.status not in admin_strings:
        return False
    else:
        return True

@Client.on_message(filters.new_chat_title )
async def new_member(client: Client, message: Message):
 db = client.db_name
 collection = db.mycollection
 doc = collection.find_one({'chat_title':f"{message.chat.title }"})
 if doc['event'] == "on":
     chat_titel = message.chat.title
     await message.reply(f"🆕 chat title:\n{chat_titel} ")

@Client.on_message(filters.pinned_message )
async def new_member(client: Client, message: Message):
 db = client.db_name
 collection = db.mycollection
 doc = collection.find_one({'chat_title':f"{message.chat.title }"})
 if doc['event'] == "on":
     chat_titel = message.chat.title
     chat = message.chat.pinned_message
     await message.reply(f"New pinned message in {chat_titel}:\n{chat}")
     

@Client.on_message(filters.command("link") & ~filters.private)
async def link (client,message):
 chat = await client.get_chat(message.chat.id)
 await message.reply(chat.invite_link)

@Client.on_message(filters.command("id"))
async def id (client,message):
   await message.reply_text(f"User_ID: {message.from_user.id}\nUsername: {message.from_user.username}")



@Client.on_message(filters.command("chat_info") & ~filters.private)
async def edit (client,message):
     chat = message.chat
     chat = await client.get_chat(chat.id)
     count = await client.get_chat_members_count(chat.id)
     await client.send_video(chat.id , "plugins/images/animation.gif.mp4", caption=f"`―――――――――――[INFO]―――――――――――\nChat Title: {chat.title}\nChat ID: {chat.id}\nDesciption: {chat.description}\nMembers: {count}\n――――――――――――――――――――――――――――`")


  
@Client.on_message(filters.left_chat_member)
async def new_member(client: Client, message: Message):
    db = mongo.db_name
    collection = db.mycollection
    doc = collection.find_one({'chat_title':f"{message.chat.title }"})
    if doc['event'] == "on":
     chat_titel = message.chat.title
     await client.send_photo(message.chat.id,"plugins/images/photo_2024-03-16_22-36-01.jpg", caption=f"`―――――――――――[INFO]―――――――――――\n@{message.left_chat_member.username} left the {chat_titel}\n――――――――――――――――――――――――――――`")
 


@Client.on_message(filters.command("pin") & ~filters.private)
async def pin_message(client, message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        get_group = await client.get_chat(chat_id)
        can_pin = await admin_check(message)
        if can_pin:
            try:
                if message.reply_to_message:
                    disable_notification = True
                    if len(message.command) >= 2 and message.command[1] in ['alert', 'notify', 'loud']:
                        disable_notification = False
                    await client.pin_chat_message(
                        message.chat.id,
                        message.reply_to_message.message_id,
                        disable_notification=disable_notification
                    )
                    await message.edit(
                            f"**Message Pinned**\n"
                            f"Chat: `{get_group.title}` (`{chat_id}`)"
                            )
                else:
                    await message.edit("`Reply to a message to pin`")
                    await asyncio.sleep(5)
                    await message.delete()
            except Exception as e:
                await message.edit("`Error!`\n"
                            f"**Log:** `{e}`"
                        )
                return
        else:
            await message.edit("`permission denied`")
            await asyncio.sleep(5)
            await message.delete()   
    else:
        await message.delete()





