from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.translate import Translator
from bot.utils import log

from bot.db.models import HistoryEntry
from bot.db.requests import add_history, get_history
from bot.keyboards.user_keyboard import make_back_keyboard, make_main_menu_keyboard
from bot.states import TranslateStates

router = Router()
translator = Translator()

@router.message(commands=['start'])
async def start_message_handler(message: Message) -> None:
    await message.answer('Привет! Выберите режим перевода.', reply_markup=make_main_menu_keyboard())

@router.message(commands=['cancel'])
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Выберите режим перевода.', reply_markup=make_main_menu_keyboard())

@router.callback_query(text='back_menu')
async def back_menu_callback(call: CallbackQuery) -> None:
    await call.message.edit_text(text='Выберите режим перевода.', reply_markup=make_main_menu_keyboard())

@router.callback_query(text='translate_history')
async def show_history_callback(call: CallbackQuery, session: AsyncSession) -> None:
    text = '<b>История последних переводов: </b>\n\n'
    
    history = await get_history(session, call.from_user.id)
    if len(history) >= 1:
        history.reverse()
        entry: HistoryEntry
        for entry in history:
            text += f'<i>{entry.translate_from}</i><b> -> </b><i>{entry.translate_to}</i>\n\n'
            
        await call.message.edit_text(text=text, reply_markup=make_back_keyboard())
    else:
        await call.message.edit_text('История недоступна, т.к. вы еще не пользовались переводчиком', reply_markup=make_back_keyboard())

@router.callback_query(text='ru_to_en')
async def ru_to_en_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Выбран режим перевода с Русского на Английский.\n\nДля выхода введите /cancel')
    await state.set_state(TranslateStates.ru_to_en)
    await call.message.delete()
    
@router.callback_query(text='en_to_ru')
async def en_to_ru_callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.answer('Выбран режим перевода с Английского на Русский.\n\nДля выхода введите /cancel')
    await state.set_state(TranslateStates.en_to_ru)
    await call.message.delete()
    
@router.message(TranslateStates.ru_to_en)
async def ru_to_en_handler(message: Message, session: AsyncSession) -> None:
    translate = translator.ru_to_en(message.text)
    await message.answer(translate)
    await add_history(session, message.from_user.id, message.text, translate)
    
@router.message(TranslateStates.en_to_ru)
async def en_to_ru_handler(message: Message, session: AsyncSession) -> None:
    translate = translator.en_to_ru(message.text)
    await message.answer(translate)
    await add_history(session, message.from_user.id, message.text, translate)
    
