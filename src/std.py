from powdr import PIL, Expression, Identity, WitnessColumn, FixedColumn, run
from typing import Generator

def force_bool(expr: Expression) -> PIL:
    yield expr * (1 - expr) == 0

def is_zero(x: Expression) -> Generator[Identity, None, Expression]:
    x_is_zero = WitnessColumn("x_is_zero")
    yield from force_bool(x_is_zero)
    x_inv = WitnessColumn("x_inv")
    yield x_is_zero == (1 - x * x_inv)
    yield x_is_zero * x == 0
    return x_is_zero

def test_is_zero():
    def program() -> PIL:
        foo = FixedColumn("foo", [0, 1, 2, 3])
        foo_is_zero = yield from is_zero(foo)
        assert isinstance(foo_is_zero, WitnessColumn)
    run(program, 4, "bn254")