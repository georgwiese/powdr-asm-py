from powdr import FixedColumn, WitnessColumn

def mload(x: WitnessColumn, step: FixedColumn, y: WitnessColumn):
    yield x == y
