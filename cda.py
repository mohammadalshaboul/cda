import telebot
from datetime import datetime
from telebot import types
from dateutil.relativedelta import relativedelta

TOKEN = '7679740498:AAHUQ8eZOS8amDf6KtxeFdsPnKl2rvz1oG4'
bot = telebot.TeleBot(TOKEN)

required_channels = ['@zajal2']
verified_users = set()  # لتتبع من أرسل /start وتم التحقق منه

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    if chat_id in verified_users:
        bot.send_message(chat_id, "ارسل عمرك بالصيغة التالية:\nهكذا 01/01/1999")
        return

    welcome_text = (
        "مرحباً بك في بوت حساب حياتك!\n\n"
        "لتتمكن من استخدام البوت، يجب عليك الاشتراك في القنوات التالية."
    )

    markup = types.InlineKeyboardMarkup()
    for channel in required_channels:
        button = types.InlineKeyboardButton(text=f"اشترك في {channel}", url=f"https://t.me/{channel[1:]}")
        markup.add(button)

    check_button = types.InlineKeyboardButton(text="التحقق من الاشتراك", callback_data="check_subscription")
    markup.add(check_button)

    bot.send_message(chat_id, welcome_text, reply_markup=markup)

def check_subscription(chat_id):
    for channel in required_channels:
        try:
            member = bot.get_chat_member(channel, chat_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def callback_check_subscription(call):
    chat_id = call.message.chat.id
    if check_subscription(chat_id):
        verified_users.add(chat_id)
        bot.answer_callback_query(call.id, "تم التحقق من الاشتراك. يمكنك الآن استخدام البوت.")
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        bot.send_message(chat_id, "ارسل عمرك بالصيغة التالية:\nهكذا 01/01/1999")
    else:
        bot.answer_callback_query(call.id, "لم يتم الاشتراك في جميع القنوات. الرجاء الاشتراك أولاً.")

@bot.message_handler(func=lambda message: True)
def calculate_life_stats(message):
    chat_id = message.chat.id

    if chat_id not in verified_users:
        bot.send_message(chat_id, "من فضلك، ابدأ باستخدام الأمر /start أولاً.")
        return

    try:
        birth_date = datetime.strptime(message.text.strip(), "%d/%m/%Y")
        now = datetime.now()

        age = relativedelta(now, birth_date)
        delta = now - birth_date

        days = delta.days
        seconds = int(delta.total_seconds())
        minutes = seconds // 60
        hours = seconds // 3600
        months = age.years * 12 + age.months

        meals = days * 3
        sleep_hours = days * 8
        laughs = days * 10
        heart_beats = int(seconds * 1.05)
        breaths = int(minutes * 18)
        milliseconds = seconds * 1000

        zodiac_sign = get_zodiac_sign(birth_date.day, birth_date.month)

        this_year_birthday = birth_date.replace(year=now.year)
        if this_year_birthday < now:
            this_year_birthday = this_year_birthday.replace(year=now.year + 1)
        time_to_birthday = relativedelta(this_year_birthday, now)
        birthday_remaining = f"يبقى على عيد ميلادك: {time_to_birthday.months} شهر و {time_to_birthday.days} يوم 🎂"

        response = (
            f"عمرك الحالي: {age.years} سنة، {age.months} شهر، و {age.days} يوم 🎉\n"
            f"{birthday_remaining}\n"
            f"برجك الفلكي: {zodiac_sign} ♈️\n\n"
            f"عدد الأشهر التي عشتها: {months} شهر 🕒\n"
            f"- عدد الأيام التي عشتها: {days} يوم 🗓️\n"
            f"- عدد الساعات التي عشتها: {hours} ساعة ⏰\n"
            f"- عدد الدقائق التي عشتها: {minutes} دقيقة ⏳\n"
            f"- عدد الثواني التي عشتها: {seconds} ثانية ⏱️\n"
            f"- عدد أجزاء الثانية التي عشتها: {milliseconds} ميلي ثانية ⚡\n\n"
            f"- عدد وجبات الطعام التي أكلتها: {meals} وجبة 🍽️\n"
            f"- عدد الساعات التي نمتها: {sleep_hours} ساعة 🛌\n"
            f"- عدد الضحكات التي ضحكتها: {laughs} ضحكة 😂\n"
            f"- عدد نبضات القلب التي نبضتها: {heart_beats} نبضة ❤️\n"
            f"- تنفست حوالي: {breaths} مرة 🌬️"
        )
        bot.reply_to(message, response)

    except ValueError:
        bot.reply_to(message, "صيغة التاريخ غير صحيحة. الرجاء إدخال التاريخ هكذا: يوم/شهر/سنة (مثلاً: 04/05/2000)")

def get_zodiac_sign(day, month):
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "الجدي"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "الدلو"
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return "الحوت"
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "الحمل"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "الثور"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "الجوزاء"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "السرطان"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "الأسد"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "العذراء"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "الميزان"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "العقرب"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "القوس"

if __name__ == "__main__":
    bot.infinity_polling()
