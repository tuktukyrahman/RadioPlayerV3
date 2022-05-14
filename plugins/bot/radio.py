import asyncio
from config import Config, STREAM
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME
from pyrogram import Client, filters, emoji

ADMINS=Config.ADMINS
CHAT_ID=Config.CHAT_ID
LOG_GROUP=Config.LOG_GROUP

async def is_admin(_, client, message: Message):
    admins = await mp.get_admins(CHAT_ID)
    if message.from_user is None and message.sender_chat:
        return True
    if message.from_user.id in admins:
        return True
    else:
        return False

ADMINS_FILTER = filters.create(is_admin)


@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def radio(_, message: Message):
    if 1 in RADIO:
        k=await message.reply_text(f"{emoji.ROBOT} **Please Stop Existing Radio Stream!**")
        await mp.delete(k)
        await message.delete()
        return
    await mp.start_radio()
    k=await message.reply_text(f"{emoji.CHECK_MARK_BUTTON} **Radio Stream Started :** \n<code>{STREAM}</code>")
    await mp.delete(k)
    await mp.delete(message)

@Client.on_message(filters.command(["stopradio", f"stopradio@{USERNAME}"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def stop(_, message: Message):
    if 0 in RADIO:
        k=await message.reply_text(f"{emoji.ROBOT} **Please Start A Radio Stream First!**")
        await mp.delete(k)
        await mp.delete(message)
        return
    await mp.stop_radio()
    k=await message.reply_text(f"{emoji.CROSS_MARK_BUTTON} **Radio Stream Ended Successfully!**")
    await mp.delete(k)
    await mp.delete(message)
