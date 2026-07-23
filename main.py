import os
import logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Функция, которая отвечает на команду /oclock
async def oclock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    await update.message.reply_text(f"⏰ Сейчас: {time_str}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот готов! Напиши /oclock, чтобы узнать текущее время.")

if __name__ == '__main__':
    if not TOKEN:
        print("Ошибка: BOT_TOKEN не найден!")
    else:
        # Запускаем веб-сервер для Render
        t = Thread(target=run_web_server)
        t.daemon = True
        t.start()

        application = Application.builder().token(TOKEN).build()
        
        # Добавляем команды
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("oclock", oclock_command))

        print("Бот успешно запущен!")
        application.run_polling()
        
