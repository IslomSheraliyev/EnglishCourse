from datetime import timedelta, datetime

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import TeleBot
from telebot.types import InputMediaPhoto

from constants import admin, low_quality, high_quality
from inline_markup import create_inline_markup
from strings import Strings as Strings


class Bot:
    def __init__(self):
        self.strings = Strings()
        self.scheduler = BackgroundScheduler()
        self.bot = TeleBot(token=self.strings.token)

    def start(self, message):
        self.bot.send_media_group(
            chat_id=message.chat.id,
            media=[
                InputMediaPhoto(
                    open("assets/AsilbekYusupov.jpg", 'rb'),
                    self.strings.start,
                    parse_mode=self.strings.html
                ),
                InputMediaPhoto(open("assets/IeltsResult.jpg", 'rb')),
            ]
        )

        self.bot.send_message(
            chat_id=message.chat.id,
            text=self.strings.ask_for_format,
            reply_markup=create_inline_markup(
                {
                    self.strings.px360: self.strings.low_quality,
                    self.strings.px720: self.strings.high_quality
                }
            ),
            parse_mode=self.strings.html
        )

    def send_first_message(self, chat_id):
        if chat_id:
            try:
                self.bot.send_message(
                    chat_id=chat_id,
                    text=self.strings.delayed_first,
                    parse_mode=self.strings.html
                )
            except Exception as e:
                print(e)

    def send_second_message(self, chat_id):
        if chat_id:
            try:
                self.bot.send_message(
                    chat_id=chat_id,
                    text=self.strings.delayed_second,
                    parse_mode=self.strings.html
                )
            except Exception as e:
                print(e)

    def send_third_message(self, chat_id):
        if chat_id:
            try:
                self.bot.send_message(
                    chat_id=chat_id,
                    text=self.strings.delayed_third,
                    parse_mode=self.strings.html
                )
            except Exception as e:
                print(e)

    def schedule_one_hour_message(self, chat_id):
        run_date = datetime.now(pytz.timezone('Asia/Tashkent')) + timedelta(hours=1)
        self.scheduler.add_job(self.send_first_message, 'date', run_date=run_date, args=[chat_id])

    def schedule_three_hour_message(self, chat_id):
        run_date = datetime.now(pytz.timezone('Asia/Tashkent')) + timedelta(hours=3)
        self.scheduler.add_job(self.send_second_message, 'date', run_date=run_date, args=[chat_id])

    def schedule_twelve_hour_message(self, chat_id):
        run_date = datetime.now(pytz.timezone('Asia/Tashkent')) + timedelta(hours=12)
        self.scheduler.add_job(self.send_third_message, 'date', run_date=run_date, args=[chat_id])

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start(message)

        @self.bot.message_handler(content_types=['text', 'video', 'photo'])
        def get_id(message):
            print(message.id)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback(call):

            if call.data == self.strings.low_quality:
                self.bot.copy_message(
                    chat_id=call.message.chat.id,
                    from_chat_id=admin,
                    message_id=low_quality
                )
            elif call.data == self.strings.high_quality:
                self.bot.copy_message(
                    chat_id=call.message.chat.id,
                    from_chat_id=admin,
                    message_id=high_quality
                )

            if call.data in [self.strings.low_quality, self.strings.high_quality]:
                self.schedule_one_hour_message(call.message.chat.id)
                self.schedule_three_hour_message(call.message.chat.id)
                self.schedule_twelve_hour_message(call.message.chat.id)
                self.scheduler.start()

        self.bot.infinity_polling(
            timeout=10,
            long_polling_timeout=5
        )


if __name__ == '__main__':
    bot = Bot()
    bot.run()
