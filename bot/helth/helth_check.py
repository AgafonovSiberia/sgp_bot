from aiogram import Bot
import sys
import asyncio
from aiogram.exceptions import TelegramRetryAfter, TelegramUnauthorizedError,TelegramBadRequest
from aiohttp.client_exceptions import ClientConnectorError
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout)


async def main():
    try:
        token = sys.argv[1]
        bot = Bot(token)
        await bot.get_me()
    except TelegramRetryAfter:
        logger.info(f"Flood control exceeded on method - do not restart")
        exit(0)
    except ClientConnectorError:
        logger.error(f"Cannot connect to host api.telegram.org:443")
        exit(1)
    except TelegramBadRequest as tbr:
        logger.error(f"{tbr.message}")
        exit(1)
    except TelegramUnauthorizedError:
        logger.error(f"Invalid BotToken")
        exit(1)
    except Exception as e:
        logger.error(f"Unknown error {str(e)}")
        exit(1)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

