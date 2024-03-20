from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton
from pyrogram.types import CallbackQuery



@Client.on_message(filters.command("edit"))
async def edit (client,message):
    keybord=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("edit", callback_data="edit")],
        ])
    await message.reply(text = "edited" , reply_markup = keybord)


@Client.on_callback_query(filters.regex('edit'))
async def switch (client ,callback_query: CallbackQuery):
   if callback_query.data == "edit":
    await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id,text = "this text has been edited")




    