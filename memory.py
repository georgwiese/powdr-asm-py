from powdr import FixedColumn, WitnessColumn, PIL, star, lookup, permutation, NumberExpression, Expression
from std import force_bool
from typing import List


def mstore(step: WitnessColumn, addr: FixedColumn, value: WitnessColumn) -> PIL:
    m_addr = WitnessColumn("m_addr")
    m_step = WitnessColumn("m_step")
    m_value = WitnessColumn("m_value")
    m_is_write = WitnessColumn("m_is_write")
    yield permutation([NumberExpression(1), addr, step, value], [m_is_write, m_addr, m_step, m_value])


def mload(step: WitnessColumn, addr: FixedColumn, value: WitnessColumn) -> PIL:
    m_addr = WitnessColumn("m_addr")
    m_step = WitnessColumn("m_step")
    m_value = WitnessColumn("m_value")
    m_is_write = WitnessColumn("m_is_write")
    yield permutation([NumberExpression(0), addr, step, value], [m_is_write, m_addr, m_step, m_value])


def memory(selectors: List[Expression]) -> PIL:
    
    # =============== read-write memory =======================
    # Read-write memory. Columns are sorted by addr and
    # then by step. change is 1 if and only if addr changes
    # in the next row.
    # Note that these column names are used by witgen to detect
    # this machine...
    m_addr = WitnessColumn("m_addr")
    m_step = WitnessColumn("m_step")
    m_change = WitnessColumn("m_change")
    m_value = WitnessColumn("m_value")

    # Memory operation flags
    m_is_write = WitnessColumn("m_is_write")
    yield from force_bool(m_is_write)

    # is_write can only be 1 if a selector is active
    is_mem_op = sum(selectors)
    yield from force_bool(is_mem_op)
    yield (1 - is_mem_op) * m_is_write == 0

    # If the next line is a not a write and we have an address change,
    # then the value is zero.
    yield (1 - m_is_write.n) * m_change * m_value.n == 0

    # change has to be 1 in the last row, so that a first read on row zero is constrained to return 0
    FIRST = FixedColumn("FIRST", [1] + star([0]))
    LAST = FIRST.n
    yield (1 - m_change) * LAST == 0

    # If the next line is a read and we stay at the same address, then the
    # value cannot change.
    yield (1 - m_is_write.n) * (1 - m_change) * (m_value.n - m_value) == 0

    m_diff_lower = WitnessColumn("m_diff_lower")
    m_diff_upper = WitnessColumn("m_diff_upper")

    BIT16 = FixedColumn("BIT16", "i & 0xffff")
    yield lookup([m_diff_lower], [BIT16])
    yield lookup([m_diff_upper], [BIT16])

    yield from force_bool(m_change)

    # if change is zero, addr has to stay the same.
    yield (m_addr.n - m_addr) * (1 - m_change) == 0

    # Except for the last row, if change is 1, then addr has to increase,
    # if it is zero, step has to increase.
    # `m_diff_upper * 2**16 + m_diff_lower` has to be equal to the difference **minus one**.
    # Since we know that both addr and step can only be 32-Bit, this enforces that
    # the values are strictly increasing.
    diff = (m_change * (m_addr.n - m_addr) + (1 - m_change) * (m_step.n - m_step))
    yield (1 - LAST) * (diff - 1 - m_diff_upper * 2**16 - m_diff_lower) == 0