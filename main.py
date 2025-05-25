import telebot
from config import TOKEN
from telebot import types
from football_api import get_today_matches

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
        analysis = get_today_matches()
        bot.send_message(message.chat.id, analysis)

    else:
        bot.send_message(message.chat.id, "دستور نامعتبره. لطفاً از منو استفاده کنید.")

print("✅ ربات با منوی اصلی اجرا شد. منتظر پیام هستم...")
bot.infinity_polling()
