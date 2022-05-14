import asyncio
from config import Config
from utils import USERNAME
from pyrogram import Client, errors
from youtubesearchpython import VideosSearch
from pyrogram.handlers import InlineQueryHandler
from pyrogram.types import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup

REPLY_MESSAGE=Config.REPLY_MESSAGE

buttons = [
            [
                InlineKeyboardButton("❔ HOW TO USE ME ❔", callback_data="help"),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/P_R_I_Y_O_O"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/P_R_I_Y_O_O"),
            ],
            [
                InlineKeyboardButton("🤖 MAKE YOUR OWN BOT 🤖", url="https://heroku.com/deploy?template=https://github.com/itspriyo/RadioPlayerV3"),
            ]
         ]


@Client.on_inline_query()
async def search(client, query):
    answers = []
    if query.query == "P_R_I_Y_O_O":
        answers.append(
            InlineQueryResultPhoto(
                title="Deploy Your Own Radio Player",
                thumb_url="-",
                photo_url="-",
                caption=f"{REPLY_MESSAGE}\n\n<b>© Powered By : \n@P_R_I_Y_O_O 👑</b>",
                reply_markup=InlineKeyboardMarkup(buttons)
                )
            )
        await query.answer(results=answers, cache_time=0)
        return
    string = query.query.lower().strip().rstrip()
    if string == "":
        await client.answer_inline_query(
            query.id,
            results=answers,
            switch_pm_text=("✍️ Type An Video Name !"),
            switch_pm_parameter="help",
            cache_time=0
        )
    else:
        videosSearch = VideosSearch(string.lower(), limit=50)
        for v in videosSearch.result()["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=v["title"],
                    description=("Duration: {} Views: {}").format(
                        v["duration"],
                        v["viewCount"]["short"]
                    ),
                    input_message_content=InputTextMessageContent(
                        "/play https://www.youtube.com/watch?v={}".format(
                            v["id"]
                        )
                    ),
                    thumb_url=v["thumbnails"][0]["url"]
                )
            )
        try:
            await query.answer(
                results=answers,
                cache_time=0
            )
        except errors.QueryIdInvalid:
            await query.answer(
                results=answers,
                cache_time=0,
                switch_pm_text=("Error: Search Timed Out!"),
                switch_pm_parameter="",
            )


__handlers__ = [
    [
        InlineQueryHandler(
            search
        )
    ]
]
