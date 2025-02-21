import asyncio
import logging
import sys

import aiogram.dispatcher.dispatcher
import dishka.integrations.aiogram

import app.core.config
from app.adapters.aiogram.campaigns.handlers import campaigns_router
from app.adapters.aiogram.handlers import main_router
from app.adapters.aiogram.menu.handlers import menu_router

if not app.core.config.config.DEBUG:
    from app.adapters.containers.production import container

else:
    from app.adapters.containers.debug import container

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bot = aiogram.Bot(token=app.core.config.config.TOKEN_TELEGRAM_API)
dp = aiogram.dispatcher.dispatcher.Dispatcher()

dp.include_routers(
    main_router,
    menu_router,
    campaigns_router,
)


async def main() -> None:
    dishka.integrations.aiogram.setup_dishka(container, dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
