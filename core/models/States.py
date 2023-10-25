from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()


class PostStates(StatesGroup):
    """
    Post state
    """
    POST_OR_ADVERTISEMENT = State()
    DATE = State()
    HOURS = State()
    HOURS_MINUTES = State()
    DELETE = State()


