# coding: utf-8

from traceback import format_exc


def ignore_exceptions(bot):
    u"""
    Catch exceptions, print them to stdout and send some message
    to chat.
    """
    def decorator(fn):
        def wrapper(request, *args, **kwargs):
            try:
                return fn(request, *args, **kwargs)
            except Exception as exc:
                print("Exception was raised:", format_exc())
                try:
                    bot.send_message(
                        request.chat.id,
                        "Ай, блять, эксепшен поймал ({})"
                        .format(exc.__class__.__name__))
                except Exception:
                    pass
        return wrapper
    return decorator
