from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery
from pyrogram import Client, filters
import random


user_id = ""
user_p = 0
bot_p = 0

def check_points(user_points, bot_points):
    if user_points == 6 or bot_points == 6:
        global user_id,user_p,bot_p
        user_id = ""
        user_p = 0
        bot_p = 0
        return True
    else:
        return False



@Client.on_callback_query(filters.regex("rps_(.*)"))
async def switch(client, callback_query: CallbackQuery):
 global user_p,bot_p
 options = ["Scissors","rock","paper"]
 computer_choice = random.choice(options)
 username = callback_query.from_user.mention
 query_id_ = callback_query.id
 game_result = check_points(user_p, bot_p)
 keybord = InlineKeyboardMarkup(
     [
         [InlineKeyboardButton("Rock 🪨 ", callback_data="rps_rock"),
         InlineKeyboardButton("Paper 📄", callback_data="rps_paper"),
         InlineKeyboardButton("scissors ✂️", callback_data="rps_scissors")],
     ]
 )

 if game_result == False:
  if callback_query.from_user.id == user_id:
      if callback_query.data.split("_", 1)[1] == computer_choice:
           await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id, text = f"`―――――――――SCORE BORD―――――――――\n{username} 👤  Vs   Bot 🤖\nTie Game!\n――――――――――――――――――――――――――――`",reply_markup = keybord)
      elif callback_query.data.split("_", 1)[1]== "rock" and computer_choice == "scissors":
              user_p += 1 
              await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id,text=f"`―――――――――SCORE BORD―――――――――\n{username}: {user_p}\nBot: {bot_p}\n――――――――――――――――――――――――――――`",reply_markup = keybord)
      elif callback_query.data.split("_", 1)[1]== "paper" and computer_choice == "rock":
              user_p += 1 
              await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id, text =f"`―――――――――SCORE BORD―――――――――\n{username}: {user_p}\nBot: {bot_p}\n――――――――――――――――――――――――――――`",reply_markup = keybord)    
      elif callback_query.data.split("_", 1)[1]== "scissors" and computer_choice == "paper":
              user_p += 1 
              await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id, text =f"`―――――――――SCORE BORD―――――――――\n{username}: {user_p}\nBot: {bot_p}\n――――――――――――――――――――――――――――`",reply_markup = keybord)
      else:
          bot_p += 1
          await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id, text =f"`―――――――――SCORE BORD―――――――――\n{username}: {user_p}\nBot: {bot_p}\n――――――――――――――――――――――――――――`",reply_markup = keybord)
  else:
         await client.answer_callback_query(callback_query_id= query_id_,text="This is not your game!🎮\n Use /rps to play!", show_alert=True)
 if user_p == 5:
    await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id, text = f"`―――――――――SCORE BORD―――――――――\n{username}: Win\nBot: Lost\n――――――――――――――――――――――――――――`")
    user_p = 0
 elif bot_p == 5:
    await client.edit_message_text(chat_id= callback_query.message.chat.id,message_id = callback_query.message.id, text = f"`―――――――――SCORE BORD―――――――――\n{username}: Lost\nBot: Win\n――――――――――――――――――――――――――――`")
    bot_p = 0

@Client.on_message(filters.command("rps"))
async def rps(client, message):
    global user_id
    user_id = message.from_user.id
    user_name = message.from_user.username
    keybord = InlineKeyboardMarkup(
             [
               [
              InlineKeyboardButton("Rock 🪨 ", callback_data="rps_rock"),
              InlineKeyboardButton("Paper 📄", callback_data="rps_paper"),
              InlineKeyboardButton("scissors ✂️", callback_data="rps_scissors")
               ]
             ]
     )
    await client.send_message(chat_id=message.chat.id,text=
         f"`―――――――――――✂️🪨📃――――――――――\n@{user_name} 👤  Vs   Bot🤖\n―――――――――――――――――――――――――――`",
         reply_markup=keybord)
     

     
 
 