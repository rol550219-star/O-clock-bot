from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from datetime import datetime, time
from zoneinfo import ZoneInfo

CHAT_ID = None

async def startoclock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID

    CHAT_ID = update.effective_chat.id

    await update.message.reply_text("🕒 Годинник увімкнено!")

    # Видаляємо старі задачі, якщо були
    for job in context.job_queue.get_jobs_by_name("clock"):
        job.schedule_removal()

    async def send_time(ctx):
        now = datetime.now(ZoneInfo("Europe/Kyiv"))
        await ctx.bot.send_message(
            chat_id=CHAT_ID,
            text=now.strftime("%H:%M")
        )

    for hour in range(24):
        context.job_queue.run_daily(
            send_time,
            time=time(hour=hour, minute=0, second=0, tzinfo=ZoneInfo("Europe/Kyiv")),
            name="clock"
        )

app.add_handler(CommandHandler("startoclock", startoclock))
