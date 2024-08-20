"""Expert
"""
import asyncio
import inspect
import os
import sys
from functools import update_wrapper
from typing import Any, Callable, Coroutine, TypeVar, cast
from expert._trade import Trade
from _logger import getLogger

_logger = getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def setup_method(f: F) -> F:
    def wrapper_func(self, *args: Any, **kwargs: Any) -> Any:
        return f(self, *args, **kwargs)

    return cast(F, update_wrapper(wrapper_func, f))


class Expert(Trade):
    """
    :param symbol: Инструмент с которым работает эксперт.
    :type symbol: `str` or `None`
    :param time_frame: Таймфрейм, по которому осуществляется торговля эксперт.
    :type time_frame: `str` or `set[str]` or `None`
    :param shift: Сдвиг относительно текущего бара, бар на котором осуществляется торговля эксперта.
    :type shift: `int`
    :param period: Период (интервал) баров на котором осуществляется торговля и/или прорисовка эксперта.
    :type period: `int`
    """
    # __dict__ = ["on_init", "on_deinit", "on_trade", "on_tick", "on_bar", "on_timer"]
    __comment: str = None

    def __init__(
            self,
            symbol: str | None,
            time_frame: str | set[str] | None = None,
            *,
            shift: int = 0,
            period: int = 1,
            magic: int = 0,
            title: str = "",
            prefix: str = "_",
            **props: dict[str, Any]
    ) -> None:
        super().__init__(symbol, **props)
        self._symbol = symbol
        self._time_frame = time_frame
        self._shift = shift
        self._period = period
        self._magic = magic
        self._title = title
        self._prefix = prefix

        # Создание асинхронных задач
        # self.__task_on_trade = asyncio.create_task(self.on_trade)
        # self.__task_on_tick = asyncio.create_task(self.on_tick)
        # self.__task_on_timer = asyncio.create_task(self.on_timer)
        # self.__task_on_bar = asyncio.create_task(self.on_bar(time_frame))

    def run(self) -> None:
        frame = inspect.stack()[1]
        mod = inspect.getmodule(frame[0])

        if mod:
            for attr in dir(mod):
                # Все объекты модуля.
                obj = mod.__dict__.get(attr)
                # Только функции модуля
                if callable(obj) and not isinstance(obj, type):
                    # Все функции модуля с декораторами или замыканиями или без них.
                    # Список иерархии объектов, функций, декораторов или замыканий.
                    qualif: list[str] = obj.__qualname__.split(".")
                    if len(qualif) > 1 and qualif[0] == self.__class__.__name__:
                        if any(
                                qualif[1] == item for item in
                                ["on_init", "on_deinit", "on_trade", "on_tick", "on_bar", "on_timer"]
                        ):
                            getattr(mod, attr)()
                            _logger.debug(f"Launch task for @{qualif[1]}:{attr}()")
                    else:
                        if any(qualif[0] == item for item in ["on_process"]):
                            getattr(mod, attr)()
                            _logger.debug(f"Launch task for {attr}()")

    @setup_method
    def on_process(self) -> None:
        print("*** expert.on_process ***")

    @setup_method
    def on_init(self, func: Callable) -> Callable:
        def inner() -> Callable:
            return func

        return inner

    def on_deinit(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_trade(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
        def inner() -> None:
            # task = asyncio.create_task(func())
            # task
            func()

            # i = 3
            # while i > 0:
            #     func()
            #     print(self, " ", i)
            #     i -= 1
            # return func()

        return inner

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]

    def on_bar(self, time_frame: str = "1h") -> Callable:
        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], None]) -> (
                Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, None]]
        ):
            def inner(*args, **kwargs) -> None:
                func(*args, **kwargs)
                print(time_frame)

            return inner

        return outer

    def on_timer(self, interval: int = 1000) -> Callable:
        def outer(func: Callable) -> Callable:
            def inner() -> None:
                func()
                print(interval)

            return inner

        return outer

    # @property
    # def magic(self) -> int:
    #     return self._magic
    #
    # @magic.setter
    # def magic(self, value: int) -> None:
    #     self._magic = value
    #
    # @property
    # def comment(self) -> str:
    #     return self.__comment
    #
    # @comment.setter
    # def comment(self, value: str) -> None:
    #     self.__comment = value + f"Magic number: {self._magic}"
