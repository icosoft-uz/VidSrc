from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Search', callback_data='search')
            ],
            [
                InlineKeyboardButton(text='Find ID', callback_data='find_id'),
                InlineKeyboardButton(text='Donate', callback_data='donate')
            ],
            [
                InlineKeyboardButton(text='Support', url='https://t.me/icofaq'),
                InlineKeyboardButton(text='Settings', callback_data='settings')
            ]
        ]
    )


def back():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='back', callback_data='main')
            ]
        ]
    )

