from aiogram.fsm.state import State

from src.domain.bot.forms.form_factory import FormFactory


class ExportForm(FormFactory):
    file = State()
