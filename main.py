import os, asyncio, datetime

from database.databases import insert_email, create_table_email
from dispatcher import dp
from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from states.states import EmailState

load_dotenv()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer('Welcome to our bot! Please write subject for email')
    await state.set_state(EmailState.subject)


@dp.message(EmailState.subject)
async def get_subject(message: Message, state: FSMContext):
    subject = message.text
    await state.update_data({
        'subject': subject
    })
    await message.answer('Write your email description')
    await state.set_state(EmailState.description)


@dp.message(EmailState.description)
async def get_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data({
        'description': description
    })
    await message.answer('Write your email send time(ex. dd.mm.yyyy hh:mm)')
    await state.set_state(EmailState.send_time)


@dp.message(EmailState.send_time)
async def get_send_time(message: Message, state: FSMContext):
    send_time = message.text
    date = list(map(int, send_time.split()[0].split('.')[::-1]))
    time = list(map(int, send_time.split()[1].split(':')))
    await state.update_data({
        'send_time': datetime.datetime(*date, *time)
    })
    await message.answer('Write your email receiver(ex. email@example.com)')
    await state.set_state(EmailState.receiver)


@dp.message(EmailState.receiver)
async def get_subject(message: Message, state: FSMContext):
    receiver = message.text
    await state.update_data({
        'receiver': receiver
    })
    data = await state.get_data()
    email_data = dict(
        subject=data['subject'],
        description=data['description'],
        send_time=data['send_time'],
        receiver=data['receiver']
    )
    insert_email(email_data)
    await state.clear()
    await message.answer('Successfully saved!')


async def main():
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token)
    create_table_email()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
