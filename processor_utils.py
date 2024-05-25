from collections.abc import Iterable
from types import MappingProxyType
from functools import partial
import inspect
from typing import Any, Callable, Iterator

from powdr import WitnessColumn, Expression

from asm_to_pil import Instruction


def _parameters_start_with_cls(parameters: MappingProxyType[str, inspect.Parameter]) -> bool:
    return len(parameters) > 0 and list(parameters)[0] == "cls"


def _collect_yielded_and_return(iterator: Iterator) -> tuple[list, Any]:
    if isinstance(iterator, tuple) or not isinstance(iterator, Iterable):
        # nothing yielded, iterator is already result
        return [], iterator

    yielded = []
    while True:
        try:
            yielded.append(next(iterator))
        except StopIteration as e:
            return yielded, e.value


def instruction(func: Callable | None = None, *, name: str | None = None):
    def _instruction(func: Callable, name: str):
        if name is None:
            name = func.__name__
        func._instruction_name = name
        signature = inspect.signature(func)
        if _parameters_start_with_cls(signature.parameters):
            func = classmethod(func)
        else:
            func = staticmethod(func)
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
            predicate=lambda x: hasattr(x, "_instruction_name")
        )

        for _, instruction_fn in instruction_fns:
            name = instruction_fn._instruction_name
            print(name)
            signature = inspect.signature(instruction_fn)
            parameters = list(signature.parameters)
            if _parameters_start_with_cls(signature.parameters):
                parameters = parameters[1:]
                args = [cls]
            else:
                args = []

            # For now, we capitalize the input var-names to stay close to the
            # template, but this should use some numbering-schema later
            # to re-use the same registers where possible.
            # Also, the inputs and output could use the same numbered namespace
            # for efficiency.
            kwargs = {
                parameter: WitnessColumn(parameter.upper()) for parameter in parameters
            }
            input_columns = list(kwargs.values())

            yielded_constraints, output_expressions = _collect_yielded_and_return(
                instruction_fn(*args, **kwargs)
            )

            if output_expressions is None:
                output_expressions = tuple()
            elif isinstance(output_expressions, Expression):
                output_expressions = (output_expressions, )

            output_columns = [WitnessColumn(f"OUT_{i}") for i in range(len(output_expressions))]
            output_constraints = [
                column == expression
                for column, expression
                in zip(output_columns, output_expressions)
            ]

            instructions.append(
                Instruction(
                    name,
                    inputs=input_columns,
                    outputs=output_columns,
                    constraints=output_constraints + yielded_constraints
                )
            )
        
        return instructions
