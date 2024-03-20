from pyrogram import filters
from pyromod import Client
from decouple import config
from datetime import datetime



APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
OWNER = config("OWNER", default=None)


bot = Client('Bot', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins = dict(root="plugins"))

now = datetime.now().time().strftime("%H:%M:%S")
date = datetime.now().strftime("%Y-%m-%d")

print(     
 "███╗   ███╗██╗██╗  ██╗██╗   ██╗    ██████╗  ██████╗ ████████╗ \n████╗ ████║██║██║ ██╔╝██║   ██║    ██╔══██╗██╔═══██╗╚══██╔══╝\n██╔████╔██║██║█████╔╝ ██║   ██║    ██████╔╝██║   ██║   ██║   \n██║╚██╔╝██║██║██╔═██╗ ██║   ██║    ██╔══██╗██║   ██║   ██║   \n██║ ╚═╝ ██║██║██║  ██╗╚██████╔╝    ██████╔╝╚██████╔╝   ██║   \n╚═╝     ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═════╝  ╚═════╝    ╚═╝"
)

@bot.on_message(filters.command('stat'))
async def stat(client,message):
 if str(message.from_user.id)== OWNER:
  await client.send_photo(message.chat.id,"plugins/images/photo_2024-03-19_12-31-00.jpg",f"`―――――――――――[STATS]―――――――――――\n• Working\n• {date}\n• {now}\n―――――――――――――――――――――――――――――`")

                                                                                                
bot.run()
        






