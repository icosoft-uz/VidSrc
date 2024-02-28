from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Search', callback_data='search')
            ],
            [
                InlineKeyboardButton(text='', callback_data='')
            ]
        ]
    )
    return button


