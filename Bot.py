import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8527414599:AAEKUAXFO7bKFd0S6KfQ30XFTym_oPl-EJ8'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class DonatState(StatesGroup):
    waiting_for_game_id = State()

def get_games_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("PUBG Mobile", callback_data="game_pubg"),
        InlineKeyboardButton("Free Fire", callback_data="game_ff"),
        InlineKeyboardButton("Mobile Legends", callback_data="game_mlbb")
    )
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Assalomu alaykum! Universal donat botiga xush kelibsiz.\nQaysi o'yinga donat qilmoqchisiz?",
        reply_markup=get_games_keyboard()
    )

@dp.callback_query_handler(text_startswith="game_")
async def process_game_selection(call: types.CallbackQuery, state: FSMContext):
    game_name = call.data.split("_")[1].upper()
    await state.update_data(selected_game=game_name)
    
    await call.message.answer(f"Siz {game_name} o'yinini tanladingiz.\nIltimos, o'yinchi ID (Player ID) raqamingizni kiriting:")
    await DonatState.waiting_for_game_id.set()
    await call.answer()

@dp.message_handler(state=DonatState.waiting_for_game_id)
async def process_game_id(message: types.Message, state: FSMContext):
    user_id = message.text
    data = await state.get_data()
    game = data.get('selected_game')
    
    await message.answer(f"O'yin: {game}\nID: {user_id}\n\nTo'lov tizimi tez kunda ulanadi.")
    await state.finish()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
