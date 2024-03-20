from pyrogram import filters,Client,enums
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from pyrogram.raw import types
from decouple import config
import os 

OWNER = int(config("OWNER", default=None))

async def is_check_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except:
        return False

async def is_sudoadmin(message) -> bool:
    client = message._client
    check_user = await client.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status
    if user_type == "member":
        return False
    if user_type == "administrator":
        add_adminperm = check_user.can_promote_members
        if add_adminperm:
            return True
        return False
    return True

@Client.on_message(filters.command("del") & ~filters.private)
async def deleteFunc(client , message):
   chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
   privileges = chat_member.privileges
   try:
    if privileges.can_delete_messages:
     if not message.reply_to_message:
         return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nReply To A Message To Delete It\n―――――――――――――――――――――――――――――`")
     await message.reply_to_message.delete()
     await message.delete() 
   except:
     await message.reply_text("`――――――――――――[ERROR]―――――――――――\nYou don't have permission !\n―――――――――――――――――――――――――――――`")
  
@Client.on_message(filters.command('ban') & filters.group)
async def ban_chat_user(client, message):
  peer = await client.resolve_peer("paura")
  if isinstance(peer, types.InputPeerUser):
   username_id = int(peer.user_id)
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nYou not admin in this group.\n―――――――――――――――――――――――――――――`")
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.id or username_id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nReply to any user message or give user id, username\n―――――――――――――――――――――――――――――`")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nCan't find you given user in this group\n―――――――――――――――――――――――――――――`")
  try:
    await client.ban_chat_member(message.chat.id, user_id)
  except:
    return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nI don't have access to ban user\n―――――――――――――――――――――――――――――`")
  await message.reply_text(f"`――――――――――――[INFO]―――――――――――\nSuccessfully banned {user.mention} from {message.chat.title}\n―――――――――――――――――――――――――――――`")


@Client.on_message(filters.command('mute') & filters.group)
async def mute_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nYou not admin in this group.\n―――――――――――――――――――――――――――――`")
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nReply to any user message or give user id, username\n―――――――――――――――――――――――――――――`")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nCan't find you given user in this group\n―――――――――――――――――――――――――――――`")
  try:
    await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
  except:
    return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nI don't have access to mute user\n―――――――――――――――――――――――――――――`")
  await message.reply_text(f"`――――――――――――[INFO]―――――――――――\nSuccessfully muted {user.mention} from {message.chat.title}\n―――――――――――――――――――――――――――――`")


@Client.on_message(filters.command(["unban", "unmute"]) & filters.group)
async def unban_chat_user(client, message):
  if not await is_check_admin(client, message.chat.id, message.from_user.id):
    return await message.reply_text('You not admin in this group.')
  if message.reply_to_message and message.reply_to_message.from_user:
    user_id = message.reply_to_message.from_user.username or message.reply_to_message.from_user.id
  else:
    try:
      user_id = message.text.split(" ", 1)[1]
    except IndexError:
      return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nReply to any user message or give user id, username\n―――――――――――――――――――――――――――――`")
  try:
    user_id = int(user_id)
  except ValueError:
    pass
  try:
    user = (await client.get_chat_member(message.chat.id, user_id)).user
  except:
    return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nCan't find you given user in this group\n―――――――――――――――――――――――――――――`")
  try:
    await client.unban_chat_member(message.chat.id, user_id)
  except:
    return await message.reply_text(f"`――――――――――――[ERROR]―――――――――――\nI don't have access to {message.command[0]} user\n―――――――――――――――――――――――――――――`")
  await message.reply_text(f"`――――――――――――[INFO]―――――――――――\nSuccessfully {message.command[0]} {user.mention} from {message.chat.title}\n―――――――――――――――――――――――――――――`")


@Client.on_message(filters.command("ban_ghosts") & ~filters.private)
async def ban_deleted_accounts(client, message):
    chat_id = message.chat.id
    deleted_users = []
    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if deleted_users:
        banned_users = 0
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await message.reply_text(f"`――――――――――――[INFO]―――――――――――\nBanned {banned_users} Deleted Accounts\n―――――――――――――――――――――――――――――`")
    else:
        await message.reply_text("`――――――――――――[ERROR]―――――――――――\nThere are no deleted accounts in this chat\n―――――――――――――――――――――――――――――`")



@Client.on_message(filters.user(OWNER) & filters.command("leave") & ~filters.private)
async def leave(client, message):
  if len(message.command) < 2:
      return await message.reply_text("`――――――――――――[ERROR]―――――――――――\nSir, you haven't provied the chat_id.\n―――――――――――――――――――――――――――――`")
  else:
    message.command.pop(0)
    keybord=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Leave Chat", callback_data="leave_chat")],
            [InlineKeyboardButton("Leave Chat Delete", callback_data="leave_chatdelete")]
        ])
    await message.reply(text = "`――――――――――――[INFO]―――――――――――\n• Leave Chat\nDes- Only leave the chat\n\n• Leave Chat Delete\nDes- Leave the chat and delete\n―――――――――――――――――――――――――――――`" , reply_markup = keybord)
    global chat_id
    chat_id = " ".join(message.command)

@Client.on_callback_query(filters.regex("leave_(.*)"))
async def leave_chat(client, callback_query: CallbackQuery):
 global chat_id
 if OWNER == callback_query.from_user.id:
  if callback_query.data.split("_", 1)[1] == "chat":
   await client.send_photo(chat_id,"plugins/images/photo_2024-03-18_13-08-29.jpg",caption="`――――――――――――[INFO]―――――――――――\nI have to go, my owner ordered  me !\nSE YA 👋, contact my owner if your have any question.\n―――――――――――――――――――――――――――――`")
   await client.leave_chat(chat_id)
  else:
   await client.send_photo(chat_id,"plugins/images/photo_2024-03-18_13-08-29.jpg",caption="`――――――――――――[INFO]―――――――――――\nI have to go, my owner ordered  me !\nSE YA 👋, contact my owner if your have any question.\nAll the bot messages will be deleted\n―――――――――――――――――――――――――――――`")
   await client.leave_chat(chat_id, delete=True)
 else:
   await client.answer_callback_query(
    callback_query.id,
    text="Hello, You are not the owner !",
    show_alert=True
)


@Client.on_message(filters.command(["rc","restrict_chat"]) & ~filters.private)
async def rc(client, message):
 keybord=InlineKeyboardMarkup(
     [
         [InlineKeyboardButton("Restrict chat", callback_data="restrict_chat")],
         [InlineKeyboardButton("Only Text", callback_data="restrict_text")]
     ])
 await client.send_message(message.chat.id,f"`――――――――――――[RESTRICT]―――――――――――\n• Restrict chat: Completely restrict chat\n• Only Text: Chat members can only send text messages and media messages.\n―――――――――――――――――――――――――――――`",reply_markup = keybord)



@Client.on_callback_query(filters.regex("restrict_(.*)"))
async def leave_chat(client, callback_query: CallbackQuery):
 if not await is_check_admin(client, callback_query.message.chat.id, callback_query.from_user.id):
  if callback_query.data.split("_", 1)[1] == "chat":
    await client.send_message(callback_query.message.chat.id,"`――――――――――――[INFO]―――――――――――\n• This chat has been completely restricted.\n―――――――――――――――――――――――――――――`")
    await client.set_chat_permissions(callback_query.from_user.id, ChatPermissions())  
  else:
    await client.send_message(callback_query.message.chat.id,"`――――――――――――[INFO]―――――――――――\n• Chat members can only send text messages and media messages.\n―――――――――――――――――――――――――――――`")
    await client.set_chat_permissions(
        callback_query.from_user.id,
        ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True
        )
    )
 else:
   await client.answer_callback_query(callback_query.id,text="Sir, you don't have permissions do so !",show_alert=True) 


@Client.on_message(filters.command(["scp","set_chat_profile"]))
async def set_profile(client, message):
 if not await is_check_admin(client, message.chat.id, message.from_user.id):
   await message.repl_text("`――――――――――――[ERROR]―――――――――――\nSir, you don't have permissions do so.\n―――――――――――――――――――――――――――――`")
 else:
  reply_message = message.reply_to_message
  if reply_message and reply_message.photo:
   file_id = reply_message.photo.file_id
   try:
    await client.download_media(file_id, file_name="downloaded_image.jpg")
    await client.set_chat_photo(message.chat.id, photo="downloads/downloaded_image.jpg")
    os.remove(f"downloads/downloaded_image.jpg")
   except:
     await message.reply_text("`――――――――――――[ERROR]―――――――――――\nSir, Bot don't have the permission to do so.\n―――――――――――――――――――――――――――――`")
  else:
    await message.repl_text("`――――――――――――[ERROR]―――――――――――\nSir, you haven't replied to a pic.\n―――――――――――――――――――――――――――――`")

    



