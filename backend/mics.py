import functools
from typing import Any, Callable
from backend.logger import common_logger

def return_none_on_error(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any | None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            common_logger.warning(f'Received exception {e}. Returning None instead')
            return None

    return wrapper
