from aiogram import Dispatcher, Bot, Router
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()
TOKEN = os.getenv("TOKEN_BOT")


bot = Bot(TOKEN, parse_mode="MARKDOWN")
dp = Dispatcher()

# create routes

admin_router = Router()
user_router = Router()
# common_router = Router()

ROOT_DIR = Path(__file__).parent
