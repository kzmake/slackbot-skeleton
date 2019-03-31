import logging
import sys

from slackbot.bot import Bot

config = {
    'format': '[%(asctime)s] %(message)s',
    'level': logging.DEBUG,
    'stream': sys.stdout,
}
logging.basicConfig(**config)

logger = logging.getLogger(__name__)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    logger.info('setup slackbot ...')
    main()
