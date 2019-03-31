import logging
import re

from slackbot_extension import Text, Emoji, respond_to, listen_to

logger = logging.getLogger(__name__)


@respond_to('^ping$', re.IGNORECASE)
def ping(message):
    """
    ^ping$
        - slackbotへの疎通確認を行う
    """
    yield Text('pong', in_thread=True, replay=True)
    return Emoji('white_check_mark')


@listen_to('^hello$', re.IGNORECASE)
def hello(message):
    """
    ^hello$
        - slackbotへの疎通確認を行う
    """
    return Text(f"hello, sender", in_thread=True)


@respond_to('^help ping$')
def help(message):
    """
    ^help ping$
        - ping系コマンドのヘルプを表示する
    """
    yield Text(f"{ping.__doc__}", in_thread=True)
    yield Text(f"{hello.__doc__}", in_thread=True)
    return Text(f"{help.__doc__}", in_thread=True)
