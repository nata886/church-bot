from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мои месяцы", callback_data="my_months")],
        [InlineKeyboardButton(text="Моя дата", callback_data="my_date")],
        [InlineKeyboardButton(text="Выбрать дату", callback_data="choose_date")],
        [InlineKeyboardButton(text="Справка", callback_data="help")]
    ])