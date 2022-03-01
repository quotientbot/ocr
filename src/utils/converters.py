from __future__ import annotations

from typing import Optional, Any
from concurrent.futures import ThreadPoolExecutor
from functools import wraps, partial
from asyncio import get_event_loop


class ToAsync:
    def __init__(self, *, executor: Optional[ThreadPoolExecutor] = None) -> None:

        self.executor = executor

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:

            loop = get_event_loop()
            if not self.executor:
                self.executor = ThreadPoolExecutor()

            func = partial(func, *args, **kwargs)

            return await loop.run_in_executor(self.executor, func)

        return wrapper
