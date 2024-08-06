from aiogram import Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.message import Message

from src.domain.bot.handlers.handler_factory import HandlerFactory
from src.infrastructure.configs.enviroment import get_environment_variables

router = Router()


class StartHandler(HandlerFactory):

    def __init__(self) -> None:
        self.config = get_environment_variables()

    async def handle(self, message: Message) -> None:
        if message.from_user.id == self.config.ADMIN_TELEGRAM_ID:
            keyboard = [[KeyboardButton(text="♻️ Обновить БД")]]
            keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

            return await message.answer(
                "Добрый день! Для обновления списка поступивших - нажмите на кнопку \"♻️ Обновить БД\"",
                reply_markup=keyboard
            )

        keyboard = [[KeyboardButton(text="🔍 Найти себя")]]
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        await message.answer(
            "Добрый день! Если хотите узнать, есть ли Вы в списке поступивших - нажмите на кнопку \"🔍 Найти себя\"", 
            reply_markup=keyboard
        )


    def register(self, dp: Dispatcher) -> None:
        router.message(CommandStart())(self.handle)
        dp.include_router(router)
