from aiogram import Bot, Dispatcher

from src.infrastructure.configs.database import get_db_connection
from src.infrastructure.configs.enviroment import get_environment_variables
from src.infrastructure.repositories.user_repository import UserRepository

from src.application.services.user_service import UserService

from src.domain.models.base_model import init

from src.interfaces.bot.handlers.start_handler import StartHandler
from src.interfaces.bot.handlers.find_me_handler import FindMeHandler
from src.interfaces.bot.handlers.export_hanlder import ExportHandler

config = get_environment_variables()
bot = Bot(config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    init()

    connection = get_db_connection().__next__()

    user_repository = UserRepository(connection)

    user_service = UserService(user_repository)

    StartHandler().register(dp)
    FindMeHandler(user_service=user_service).register(dp)
    ExportHandler(user_service=user_service).register(dp)

    await dp.start_polling(bot)
