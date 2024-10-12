# app/states.py
from aiogram.fsm.state import StatesGroup, State

class ContributionState(StatesGroup):
    waiting_for_amount = State()
