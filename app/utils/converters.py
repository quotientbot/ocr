from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Any, Callable, Optional
import asyncio

__all__ = ("to_async",)


class to_async:
    """
    Decorator to convert a blocking function into an asynchronous function that can be used with asyncio.

    Args:
        executor (Optional[ThreadPoolExecutor]): An optional ThreadPoolExecutor instance to use for running the blocking function.

    Returns:
        Callable[..., Any]: A callable object that can be used as a decorator to make the given blocking function asynchronous.
    """

    def __init__(self, *, executor: Optional[ThreadPoolExecutor] = None):
        self.executor = executor

    def __call__(self, blocking: Callable[..., Any]) -> Any:
        """
        Callable function that takes a blocking function as argument and returns an asynchronous function.

        Args:
            blocking (Callable[..., Any]): The blocking function to be converted into an asynchronous function.

        Returns:
            Any: An asynchronous function that can be used with asyncio.
        """

        @wraps(blocking)
        async def wrapper(*args: Any, **kwargs: Any):
            loop: "asyncio.AbstractEventLoop" = asyncio.get_event_loop()
            if self.executor is None:
                self.executor = ThreadPoolExecutor()

            func = partial(blocking, *args, **kwargs)

            return await loop.run_in_executor(self.executor, func)

        return wrapper
