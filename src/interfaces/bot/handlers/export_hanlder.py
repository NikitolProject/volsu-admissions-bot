import csv
import io

from aiogram import Dispatcher, Router, F
from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    ContentType, Message, Document
)
from aiogram.fsm.context import FSMContext

from src.domain.bot.handlers.handler_factory import HandlerFactory
from src.infrastructure.configs.enviroment import get_environment_variables
from src.application.schemas.pydantic.user_schema import UserSchema
from src.application.services.user_service import UserService
from src.interfaces.bot.forms.export_form import ExportForm

router = Router()


class ExportHandler(HandlerFactory):

    def __init__(self, user_service: UserService) -> None:
        self.config = get_environment_variables()
        self.user_service = user_service

    async def handle(self, message: Message, state: FSMContext) -> None:
        await state.set_state(ExportForm.file)
        await message.answer(
            "Пришлите CSV файл со следующими столбцами: СНИЛС;поступил;факультет",
            reply_markup=ReplyKeyboardRemove()
        )

    async def handle_file(self, message: Message, state: FSMContext) -> None:
        if message.content_type != ContentType.DOCUMENT:
            return await message.answer(
                "Пожалуйста, пришлите файл формата CSV со следующими столбцами: СНИЛС;поступил;факультет"
            )
        
        document = message.document
        file_id = document.file_id
        file = await message.bot.get_file(file_id)
        file_content = await message.bot.download_file(file.file_path)
        
        csv_reader = csv.DictReader(io.StringIO(file_content.read().decode('utf-8')), delimiter=';')
        
        users = []

        for row in csv_reader:
            try:
                user = UserSchema(
                    id_card=int(row['СНИЛС']),
                    faculty=row['факультет'],
                    is_entered=True if row['поступил'].lower() in ['true', '1', 'yes', 'да'] else False
                )
                users.append(user)
            except KeyError as e:
                return await message.answer(f"Ошибка в CSV файле: отсутствует столбец {e}")
            except ValueError as e:
                return await message.answer(f"Ошибка в CSV файле: неверный формат данных {e}")

        try:
            self.user_service.bulk_create(users)

            keyboard = [[KeyboardButton(text="♻️ Обновить БД")]]
            keyboard = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

            await message.answer("Данные успешно обновлены", reply_markup=keyboard)
        except Exception as e:
            await message.answer(f"Произошла ошибка при обновлении данных: {e}")

    def register(self, dp: Dispatcher) -> None:
        router.message(F.text == "♻️ Обновить БД")(self.handle)
        router.message(ExportForm.file)(self.handle_file)
        dp.include_router(router)
