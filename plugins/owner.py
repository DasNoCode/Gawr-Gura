from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton
from pyrogram.types import CallbackQuery

@Client.on_message(filters.command("owner"))
async def owner(client, message):
    keybord=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("SCORCE", callback_data="SCORCE")],
        ])
    await client.send_photo(message.chat.id,photo = "plugins/images/photo_2024-03-19_00-13-27.jpg",caption ="`――――――――――――[OWNER]――――――――――\n• NAME: DAS KUN\n• AGE: 19\n• GENDER: MALE\n• CONTACT: @Das_2005_08\n• GITHUB: Debayan08\n• EMAIL: debayanabae2005@gmail.com\n• IG: das_abae\n―――――――――――――――――――――――――――――`",reply_markup = keybord)

@Client.on_callback_query(filters.regex('SCORCE'))
async def switch (client ,callback_query: CallbackQuery):
   if callback_query.data == "SCORCE":
       await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id,text ="`――――――――――――[LINK]―――――――――――\n• LINK: https://github.com/xditya/PyrogramBot.git\n――――――――――――――――――――――――――――`")
