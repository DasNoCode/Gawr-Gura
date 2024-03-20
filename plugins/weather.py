from pyrogram import Client,filters
import requests

def get_weather(location):
  try:
   response = requests.get(f"https://wttr.in/{location}?mnTC0&lang=en")
   return response.text
  except Exception as e:
    return e

@Client.on_message(filters.command("weather"))
async def weather(client, message):
    user_name = message.from_user.username
    if len(message.command) < 2:
        return await message.reply_text(f"@{user_name} Send **/waether location** to get info ℹ️.")
    else:
     message.command.pop(0)
     location = " ".join(message.command)
     try:
      response = requests.get(f"https://wttr.in/{location}?mnTC0&lang=en")
     except Exception as e:
       return e   
     await message.reply_text(response.text)
