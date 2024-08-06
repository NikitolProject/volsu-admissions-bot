from aiogram import Dispatcher, Router, F
from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from aiogram.types.message import Message
from aiogram.fsm.context import FSMContext

from src.domain.bot.handlers.handler_factory import HandlerFactory
from src.infrastructure.configs.enviroment import get_environment_variables
from src.application.services.user_service import UserService
from src.interfaces.bot.forms.find_me_form import FindMeForm

router = Router()


class FindMeHandler(HandlerFactory):

    def __init__(self, user_service: UserService) -> None:
        self.config = get_environment_variables()
        self.user_service = user_service

    async def handle(self, message: Message, state: FSMContext) -> None:
        await state.set_state(FindMeForm.id_card)
        await message.answer(
            "Слитно напишите Ваш номер снилса, по которому вы числитесь в рейтинге",
            reply_markup=ReplyKeyboardRemove()
        )

    async def handle_id_card(self, message: Message, state: FSMContext) -> None:
        if not message.text.isdigit():
            return await message.answer("Вы должны слитно написать Ваш номер снилса, пример: 1234567")
        
        await state.clear()
        
        user_info = self.user_service.get(int(message.text))
        keyboard = [[KeyboardButton(text="🔍 Найти себя")]]
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        if user_info is None:
            return await message.answer(
                "К сожалению, Вас ещё нет в списке. Попробуйте проверить свой статус позже",
                reply_markup=keyboard
            )
        
        if not user_info.is_entered:
            return await message.answer(
                "К сожалению, Вы не смогли поступить :(",
                reply_markup=keyboard
            )
        
        return await message.answer(
            f"Поздравляем, Вы успешно поступили в ВолГУ на факультет {user_info.faculty}!🥳",
            reply_markup=keyboard
        )
    
    def register(self, dp: Dispatcher) -> None:
        router.message(F.text == "🔍 Найти себя")(self.handle)
        router.message(FindMeForm.id_card)(self.handle_id_card)
        dp.include_router(router)
