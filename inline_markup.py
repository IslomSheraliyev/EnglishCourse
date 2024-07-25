from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_inline_markup(*raws: dict) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for raw in raws:
        inline_markup = []
        for text, data in raw.items():
            inline_markup.append(InlineKeyboardButton(text=text, callback_data=data))
        markup.row(*inline_markup)
    return markup
