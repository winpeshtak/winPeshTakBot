import telebot
from config import TOKEN
from telebot import types
import json
import subprocess
import os

bot = telebot.TeleBot(TOKEN)

# ========================== START ==========================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📊 بازی‌های امروز")
    btn2 = types.KeyboardButton("👤 وضعیت اشتراک")
    btn3 = types.KeyboardButton("🛠 پشتیبانی")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "سلام! یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=markup)

# ========================== MAIN MENU HANDLER ==========================
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text == "🛠 پشتیبانی":
        bot.send_message(message.chat.id, "برای پشتیبانی به آیدی @MrAliReihani پیام بدید")

    elif message.text == "👤 وضعیت اشتراک":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🔓 اشتراک رایگان 3 روزه")
        btn2 = types.KeyboardButton("💳 تمدید اشتراک")
        btn_back = types.KeyboardButton("⬅️ بازگشت")
        markup.add(btn1, btn2)
        markup.add(btn_back)
        bot.send_message(message.chat.id, "وضعیت اشتراک را انتخاب کنید:", reply_markup=markup)

    elif message.text == "⬅️ بازگشت":
        send_welcome(message)

    elif message.text == "🔓 اشتراک رایگان 3 روزه":
        bot.send_message(message.chat.id, "فعلاً فقط نمایشی است. بزودی فعال می‌شود ✅")

    elif message.text == "💳 تمدید اشتراک":
        bot.send_message(message.chat.id, "امکان تمدید اشتراک به‌زودی فعال می‌شود 💳")

    elif message.text == "📊 بازی‌های امروز":
        bot.send_message(message.chat.id, "📥 در حال دریافت بازی‌های امروز...")

        try:
            if not os.path.exists("scrape_goal.py"):
                bot.send_message(message.chat.id, "❌ فایل scrape_goal.py پیدا نشد!")
                return

            subprocess.run(["python3", "scrape_goal.py"], check=True)

            if not os.path.exists("matches.json"):
                bot.send_message(message.chat.id, "❌ فایل matches.json پیدا نشد!")
                return

            with open("matches.json", "r", encoding="utf-8") as f:
                matches = json.load(f)

            if not matches:
                bot.send_message(message.chat.id, "❌ بازی‌ای برای امروز پیدا نشد.")
            else:
                text = "🎯 بازی‌های امروز:\n\n"
                for m in matches:
                    text += f"🕒 {m['time']} | {m['home']} vs {m['away']} ({m['league']}, {m['country']})\n"
                bot.send_message(message.chat.id, text)

        except subprocess.CalledProcessError as e:
            bot.send_message(message.chat.id, f"❌ خطا در اجرای scraper: {e}")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ خطا در دریافت بازی‌ها: {e}")

    else:
        bot.send_message(message.chat.id, "دستور نامعتبره. لطفاً از منو استفاده کنید.")

print("✅ ربات اجرا شد. منتظر پیام هستم...")
bot.infinity_polling()
