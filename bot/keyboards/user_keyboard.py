from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def make_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.row(InlineKeyboardButton(text='Русский в Английский', callback_data='ru_to_en'))
    keyboard.row(InlineKeyboardButton(text='Английский в Русский', callback_data='en_to_ru'))
    keyboard.row(InlineKeyboardButton(text='История переводов', callback_data='translate_history'))
    return keyboard.as_markup()
    
def make_back_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text='Назад', callback_data='back_menu')
    return keyboard.as_markup()