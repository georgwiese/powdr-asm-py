#from main_processor import MainProcessor
from powdr import run


from powdr import star, FixedColumn, WitnessColumn, PIL

def fib() -> PIL:
    is_last = FixedColumn("is_last", star([0]) + [1])
    x = WitnessColumn("x")
    y = WitnessColumn("y")

    yield is_last * (y.n - 1) == 0
    yield is_last * (x.n - 1) == 0
    yield (1 - is_last) * (x.n - y) == 0
    yield (1 - is_last) * (y.n - (x + y)) == 0

run(fib, 1024, "bn254")

#mp = MainProcessor()
#
#mp.attach_co_processor(hash_5)
#cpu_instructions = load("File.asm")
#mp.load_program(cpu_instructions)
#
#pil = generate_pil(mp.generate_constraints())

