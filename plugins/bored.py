from pyrogram import Client,filters
import requests

@Client.on_message(filters.command("bored"))
async def bored(client, message):
    response = requests.get("https://www.boredapi.com/api/activity/")
    data = response.json()["activity"]

    await message.reply(f"`―――――――――――[BORED]――――――――――――\n•Activity: {data}\n――――――――――――――――――――――――――――――`")

    