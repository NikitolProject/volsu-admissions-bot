from aiogram.fsm.state import State

from src.domain.bot.forms.form_factory import FormFactory


class FindMeForm(FormFactory):
    id_card = State()
