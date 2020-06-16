import asyncio
import threading
import typing as tp
from concurrent.futures import Future

from pypeln import utils as pypeln_utils


class _Namespace:
    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)


def Namespace(**kwargs) -> tp.Any:
    return _Namespace(**kwargs)


def get_running_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop()

    if not loop.is_running():

        def run():
            loop.run_forever()

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    return loop


def run_coroutine_in_loop(f_coro: tp.Callable[[], tp.Awaitable]) -> Future:
    loop = get_running_loop()

    return asyncio.run_coroutine_threadsafe(f_coro(), loop)


def run_function_in_loop(f: tp.Callable[[], tp.Any]) -> asyncio.Handle:
    loop = get_running_loop()

    return loop.call_soon_threadsafe(f)
