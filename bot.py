from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from asynctest import check_for_new_stories
from asynctest import browser_context

# Initialize bot and dispatcher
bot = Bot(token='5960584442:AAFXTpZTD6D9VIapCEyNxmok-oMPw3qc3lY')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Define the Checker class
class Checker(StatesGroup):
    waiting_for_name = State()


# Define the /checker command handler
@dp.message_handler(commands=['checker'])
async def cmd_checker(message: types.Message):
    await Checker.waiting_for_name.set()
    await bot.send_message(message.chat.id, "Enter the name of the person you want to check:")


# Define the name message handler
@dp.message_handler(state=Checker.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        result = check_for_new_stories(data['name'])
        await bot.send_message(message.chat.id, result)
    await state.finish()




# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
