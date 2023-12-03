from aiogram.fsm.state import StatesGroup, State

# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage
# memory storage
# storage = MemoryStorage()


class PostStates(StatesGroup):
    """
    Post state
    """
    WAITING_FOR_POST = State()
    POST_OR_ADVERTISEMENT = State()
    ADD_BUTTON = State()
    BUTTON_TEXT = State()
    BUTTON_LINK = State()
    DATE = State()
    HOURS = State()
    HOURS_MINUTES = State()
    DEREGISTER_ADVERTISEMENT = State()
    ALL_POST_FROM_DATE = State()
    DELETE_THE_POST = State()

