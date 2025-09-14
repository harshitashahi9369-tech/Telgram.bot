#!/usr/bin/env python3
"""
Telegram Forced Join Bot — With Today's Joined Counter
- Restart button always triggers /start
- If user joined → delete old messages & send METHOD_TEXT + today's joined count
- If not joined → show join + restart button + today's joined count
- Tracks how many users pressed /start each day
python-telegram-bot v20+
"""

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- CONFIG ----------------
BOT_TOKEN = "8282375027:AAHm8kds3NyRV4fhRxw_imoawzhDCmv32ec"

CHANNELS = [
    {"id": "@kharidobecho1", "label": "🔗 Join Group"},
    {"id": "@pornherecheap", "label": "🔞 Join Channel"},
]
# ----------------------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

METHOD_TEXT = """@MOHITPORN0BOT

1. @PornLov3rs_bot ⭐

2. @outschool_bot ⭐

3. @PomSchool2_Bot ⭐

4. @Pomextrabot ⭐

5. @XMummyBot ⭐

6. @LxMastiRobot ⭐

7. @FreepomXpom_bot ⭐

8. @Studystuffs_bot ⭐

9. @DCSuperManXBot ⭐

10. @CORN_247_BOT ⭐

11. @C0rnPub_Bot ⭐
"""

# ---------------- STORAGE ----------------
joined_today = {}

# ---------------- HELPERS ----------------
async def is_member(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        for ch in CHANNELS:
            chat_ref = ch["id"]
            member = await context.bot.get_chat_member(chat_ref, user_id)
            logger.info(f"Check member → {chat_ref} → {member.status}")
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except Exception as e:
        logger.error(f"Check member failed for {user_id}: {e}")
        return False


def join_keyboard(bot_username: str):
    buttons = []
    for ch in CHANNELS:
        if isinstance(ch["id"], str) and ch["id"].startswith("@"):
            url = f"https://t.me/{ch['id'][1:]}"
        else:
            url = "https://t.me/" + bot_username
        buttons.append([InlineKeyboardButton(ch["label"], url=url)])

    buttons.append(
        [InlineKeyboardButton("🔄 Restart", url=f"https://t.me/{bot_username}?start=1")]
    )
    return InlineKeyboardMarkup(buttons)


async def delete_bot_messages(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    try:
        async for msg in context.bot.get_chat_history(chat_id, limit=50):
            if msg.from_user and msg.from_user.id == context.bot.id:
                try:
                    await context.bot.delete_message(chat_id, msg.message_id)
                except Exception:
                    pass
    except Exception as e:
        logger.error(f"Error while cleaning messages in chat {chat_id}: {e}")


# ---------------- HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"/start received from user {user.id} ({user.username})")

    today = datetime.now().strftime("%Y-%m-%d")
    if today not in joined_today:
        joined_today[today] = []
    if user.id not in joined_today[today]:
        joined_today[today].append(user.id)

    await delete_bot_messages(chat_id, context)

    today_count = len(joined_today.get(today, []))

    if await is_member(user.id, context):
        logger.info(f"✅ User {user.id} verified → sending METHOD_TEXT + counter")
        await context.bot.send_message(
            chat_id,
            f"{METHOD_TEXT}\n\n👥 Members joined today: {today_count}"
        )
    else:
        logger.info(f"❌ User {user.id} not verified → show join again")
        await context.bot.send_message(
            chat_id,
            f"⚠️ You must join the required channel before continuing.\n\n👥 Members joined today: {today_count}",
            reply_markup=join_keyboard(context.bot.username),
        )


# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("Bot is running... Waiting for users...")
    app.run_polling()


if __name__ == "__main__":
    main()