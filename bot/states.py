from aiogram.fsm.state import State, StatesGroup

class TranslateStates(StatesGroup):
    ru_to_en = State()
    en_to_ru = State()