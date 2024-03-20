from pyrogram import Client, filters,enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message
from pyrogram.types import CallbackQuery
import pymongo
from decouple import config

MONGO_URL = config("MONGO_URL", default=None)
mongo = pymongo.MongoClient(MONGO_URL)

@Client.on_message(filters.command("event") & ~filters.private)
async def eve (client, message):
     ms_g = 'Do you want to turn the event 🎐'
     keybord=InlineKeyboardMarkup(
         [
             [InlineKeyboardButton("OFF", callback_data="event_off")],
             [InlineKeyboardButton("ON", callback_data="event_on")]
         ])
     reply = await message.reply(text = ms_g , reply_markup = keybord)
     global message_id
     message_id = reply.id
    
db_name = "chatservices"
def fetch_event(chat_title,event):
    db = mongo.db_name
    collection = db.mycollection
    doc = collection.find_one({'chat_title': chat_title})
    if doc is None:
     event_ = {'chat_title': chat_title, 'event': event}
     collection.insert_one(event_)
    elif doc['event'] != event:
     doc = collection.find_one_and_update(
     {'chat_title': chat_title},
     {'$set': {'event': event}})
    else:
        return
           
@Client.on_callback_query(filters.regex('event_(.*)'))
async def switch (client ,callback_query: CallbackQuery):
    
    chat_id = callback_query.message.chat.id 
    chat_titel = callback_query.message.chat.title 
    help_list = "`――――――――――――[HELP]――――――――――――\n\n• Prefix [ '/ ' ] \n\n[Comments] \n\n• anime [anime name]\nDes- This will give brief description about the anime with the official poster.\n\n• qr [Link/Text]\nDes- Give text or link it will convert them into QR code.\n\n• bored\nDes- It will give you a certain task to do.\n\n• fact\nDes- It will give you fun fact.\n\n• jokes\nDes- It will give you a funny joke.\n\n• waifu \nDes- It will give waifus.\n\n• whatanime [Replied anime clip or Gif]\nDes- It will give the anime name of the clip or Gif.\n\n• voice [Text]\nDes- Text -> Audio\n\n• Translate or t [Text/Replied message]\nDes- It will translate the message into any languages \n\n•yt_dl [Link]\nDes- Download YouTube videos and audios.\n\n•ig_dl [Link]\nDes- Download Instagram videos and audios.\n\n• profile\nDes- Give user's profile Picture and usename and use id \n\n• event\nDes- Welcome message and Good Bye message \n\n• pin [Text]\nDes- Pin the message.\n\n• chat_info\nDes- Chat profile picture,id and title \n\n• link\nDes- provide the chat invite Link \n\n• id\nDes- Give your id and username\n\n• rps \nDes- Rock Paper Scissor Game\n\n• tic_tac_toe\nDes- Tic Tac Toe Game \n――――――――――――――――――――――――――――――`"
    input = callback_query.data.split("_", 1)[1]
    user = await client.get_chat_member(chat_id, callback_query.from_user.id)
    if user.status == enums.ChatMemberStatus.OWNER or user.status == enums.ChatMemberStatus.ADMINISTRATOR :
     if input == "on":
          fetch_event(chat_titel, input)
          await client.edit_message_text(callback_query.message.chat.id,message_id,text= f"Event has been turned **on** in {chat_titel}")
     elif input == "help":
         await client.send_message(chat_id= callback_query.message.chat.id,text = help_list)
     elif input == "off":
          fetch_event(chat_titel, input)
          await client.edit_message_text(callback_query.message.chat.id,message_id,text= f"Event has been turned **off** in {chat_titel}")
    else:
       await client.send_message(chat_id,"**You don't have admin permitions")


#https://docs.pyrogram.org/api/filters#module-pyrogram.filters

@Client.on_message(filters.new_chat_members)
async def new_member(client: Client, message: Message):
     db = mongo.db_name
     collection = db.mycollection
     chat_titel = message.chat.title
     btn =InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Help-list", callback_data="event_help")]
    ])
     doc = collection.find_one({'chat_title':f"{message.chat.title }"})
     for member in message.new_chat_members:
        if member.is_bot == True:
         keybord=InlineKeyboardMarkup(
          [
              [InlineKeyboardButton("Support Group", url = "https://t.me/+77-e0j4mdhRjOTdl")],
              [InlineKeyboardButton("Help List", callback_data="event_help")]
          ])
         await client.send_photo(
         chat_id=message.chat.id,
         photo="plugins/images/photo_2024-03-16_22-36-14.jpg",
         caption="`――――――――――――[INFO]―――――――――――\nHello, I am Gawr Gura Bot. Nice to meet you all.\n• Click on the support group button to enter the support the group. \n• Click on help button to get the help list.\n―――――――――――――――――――――――――――――`",
         reply_markup = keybord)
     if doc['event'] == "on":
       for member in message.new_chat_members:
         if member.is_bot == False:
          reply = await client.send_photo(
          chat_id=message.chat.id,
          photo="plugins/images/photo_2024-03-16_22-36-14.jpg",
          caption=f"`――――――――――――[INFO]―――――――――――\nWelcome @{member.username} to {chat_titel} 🎉\n―――――――――――――――――――――――――――――`",
          reply_markup = btn)
          global msg
          msg = reply.id
     else:
        return






     