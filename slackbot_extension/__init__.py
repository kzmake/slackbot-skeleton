import logging
import re
from dataclasses import dataclass

from slackbot.manager import PluginsManager

logger = logging.getLogger(__name__)


@dataclass
class Text:
    body: str
    in_thread: bool = False
    replay: bool = False


@dataclass
class Emoji:
    emoji: str


def send_text(message, value: Text):
    """メッセージ（Text）の送信処理を行う"""
    if value.replay:
        message.reply(value.body, in_thread=value.in_thread)
    else:
        if value.in_thread:
            message.send(value.body, thread_ts=message.thread_ts)
        else:
            message.send(value.body)


def send_emoji(message, value: Emoji):
    """メッセージ（Emoji）の送信処理を行う"""
    message.react(value.emoji)


def send_response(message, values):
    """メッセージの送信処理を行う"""
    if values is None:
        return

    elif isinstance(values, Text):
        send_text(message, values)

    elif isinstance(values, Emoji):
        send_emoji(message, values)

    else:
        while True:
            try:
                value = next(values)
            except StopIteration as e:
                value = e.value

            if isinstance(value, Text):
                send_text(message, value)

            if isinstance(value, Emoji):
                send_emoji(message, value)


# --------------------
#  modified decorator
# --------------------
def respond_to(matchstr, flags=0):
    def wrapper(func):
        def command_func(message, *args):
            logger.info(f"受信: {message.body}")

            generator = func(message, *args)
            send_response(message, generator)

        PluginsManager.commands['respond_to'][re.compile(matchstr, flags)] = command_func
        logger.info(f"registered respond_to plugin '{func.__name__}' to '{matchstr}'")
        return func

    return wrapper


def listen_to(matchstr, flags=0):
    def wrapper(func):
        def command_func(message, *args):
            logger.info(f"受信: {message.body}")

            generator = func(message, *args)
            send_response(message, generator)

        PluginsManager.commands['listen_to'][re.compile(matchstr, flags)] = command_func
        logger.info(f"registered listen_to plugin '{func.__name__}' to '{matchstr}'")
        return func

    return wrapper
