from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import CallbackQuery
from pyrogram import Client, filters,enums

player = "❌"
bot = "⭕️"
user_id = 0
board = {1: '⬜️', 2: '⬜️', 3: '⬜️',
         4: '⬜️', 5: '⬜️', 6: '⬜️',
         7: '⬜️', 8: '⬜️', 9: '⬜️'}


def insertLetter(letter, position):
    board[position] = letter

def clear():
    global board
    for key in board.keys():
        board[key] = '⬜️'

def checkDraw():
    for key in board.keys():  # Now the loop should work properly
        if (board[key] == '⬜️'):
            return False
    return True

def spaceIsFree(position):
    pos = int(position)
    if board[pos] == '⬜️':
        return True
    else:
        return False

def checkForWin():
    if (board[1] == board[2] and board[1] == board[3] and board[1] != '⬜️'):
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] != '⬜️'):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] != '⬜️'):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] != '⬜️'):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] != '⬜️'):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] != '⬜️'):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] != '⬜️'):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] != '⬜️'):
        return True
    else:
        return False


def checkWhichMarkWon(mark):
    if board[1] == board[2] and board[1] == board[3] and board[1] == mark:
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] == mark):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] == mark):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] == mark):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] == mark):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] == mark):
        return True
    else:
        return False

def compMove():
    bestScore = -800
    bestMove = 0
    for key in board.keys():
        if (board[key] == '⬜️'):
            board[key] = bot
            score = minimax(board, 0, False)
            board[key] = '⬜️'
            if (score > bestScore):
                bestScore = score
                bestMove = key

    insertLetter(bot, bestMove)
    
    return


def minimax(board, depth, isMaximizing):
    if (checkWhichMarkWon(bot)):
        return 1
    elif (checkWhichMarkWon(player)):
        return -1
    elif (checkDraw()):
        return 0

    if (isMaximizing):
        bestScore = -800
        for key in board.keys():
            if (board[key] == '⬜️'):
                board[key] = bot
                score = minimax(board, depth + 1, False)
                board[key] = '⬜️'
                if (score > bestScore):
                    bestScore = score
        return bestScore

    else:
        bestScore = 800
        for key in board.keys():
            if (board[key] == '⬜️'):
                board[key] = player
                score = minimax(board, depth + 1, True)
                board[key] = '⬜️'
                if (score < bestScore):
                    bestScore = score
        return bestScore

   
@Client.on_message(filters.command(["tic_tac_toe", "ttt"]))
async def rps(client, message):
    global user_id
    user_id = message.from_user.id
    keyboard_ = InlineKeyboardMarkup([
      [InlineKeyboardButton(f"{board[1]}", callback_data='T_1'),
       InlineKeyboardButton(f"{board[2]}", callback_data='T_2'),
       InlineKeyboardButton(f"{board[3]}", callback_data='T_3')],
      [InlineKeyboardButton(f"{board[4]}", callback_data='T_4'),
       InlineKeyboardButton(f"{board[5]}", callback_data='T_5'),
       InlineKeyboardButton(f"{board[6]}", callback_data='T_6')],
      [InlineKeyboardButton(f"{board[7]}", callback_data='T_7'),
       InlineKeyboardButton(f"{board[8]}", callback_data='T_8'),
       InlineKeyboardButton(f"{board[9]}", callback_data='T_9')]
     ])
    user_name = message.from_user.username
    await message.reply_text(
        f"`―――――――――SCORE BORD―――――――――\n@{user_name} 👤  Vs   Bot🤖\n――――――――――――――――――――――――――――`",
        reply_markup=keyboard_,
        parse_mode=enums.ParseMode.MARKDOWN
    )




@Client.on_callback_query(filters.regex("T_(.*)"))
async def switch1(client, callback_query: CallbackQuery):
    username = callback_query.from_user.mention
    if callback_query.from_user.id == user_id:
     if spaceIsFree(int(callback_query.data.split("_", 1)[1])):
       position = int(callback_query.data.split("_", 1)[1])
       insertLetter(player, position)
       compMove()
       keyboard_ = InlineKeyboardMarkup([
           [InlineKeyboardButton(f"{board[1]}", callback_data='T_1'),
            InlineKeyboardButton(f"{board[2]}", callback_data='T_2'),
            InlineKeyboardButton(f"{board[3]}", callback_data='T_3')],
           [InlineKeyboardButton(f"{board[4]}", callback_data='T_4'),
            InlineKeyboardButton(f"{board[5]}", callback_data='T_5'),
            InlineKeyboardButton(f"{board[6]}", callback_data='T_6')],
           [InlineKeyboardButton(f"{board[7]}", callback_data='T_7'),
            InlineKeyboardButton(f"{board[8]}", callback_data='T_8'),
            InlineKeyboardButton(f"{board[9]}", callback_data='T_9')]
          ])
       await client.edit_message_text(
           chat_id=callback_query.message.chat.id,
           message_id=callback_query.message.id,
           text=f"`―――――――――SCORE BORD―――――――――\n{username} 👤  Vs   Bot 🤖\n――――――――――――――――――――――――――――`",
           reply_markup=keyboard_
        )  
     if (checkDraw()):
          await client.edit_message_text(
              chat_id=callback_query.message.chat.id,
              message_id=callback_query.message.id,
              text=f"`―――――――――SCORE BORD―――――――――\n{username} 👤  Vs   Bot 🤖\nDraw Match!\n――――――――――――――――――――――――――――`"
           )
          clear()
     if checkForWin():
         if bot == "⭕️":
          await client.edit_message_text(
              chat_id=callback_query.message.chat.id,
              message_id=callback_query.message.id,
              text=f"`―――――――――SCORE BORD―――――――――\n{username}: Lost\nBot: Win\n――――――――――――――――――――――――――――`"
           )


          clear()
 
         else:
          await client.edit_message_text(
              chat_id=callback_query.message.chat.id,
              message_id=callback_query.message.id,
              text=f"`―――――――――SCORE BORD―――――――――\n{username}: Win\nBot: Lost\n――――――――――――――――――――――――――――`"
           )
          clear()
    else:
     await client.answer_callback_query(callback_query_id= callback_query.id,text="This is not your game!🎮\n Use /tic_tac_to to play!", show_alert=True)
 
 