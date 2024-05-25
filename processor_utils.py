from functools import partial
import inspect
from typing import Callable

from asm_to_pil import Instruction


def instruction(func: Callable | None = None, *, name: str | None = None):
    def _instruction(func: Callable, name: str):
        if name is None:
            name = func.__name__
        func = staticmethod(func)
        func.__instruction_name = name
        return func

    if func is None:
        return partial(_instruction, name=name)
    else:
        return _instruction(func, name=name)


class AbstractProcessor:
    _instructions = {}

    @classmethod
    def get_instructions(cls):
        instructions = []
        instruction_fns = inspect.getmembers(
            cls,
            predicate=lambda x: hasattr(x, "__instruction_name")
        )

        instructions.append(
            Instruction()
        )
        
        return instructions
