from typing import Iterator


class Register:
    pass

class ProgramCounter(Register):
    pass

class MainProcessor:
    def attach_co_processor(self, co_processor: CoProcessor):
        pass

    def __init__(self, ):
        self.pc = ProgramCounter()
        self.assignment_register = []
        self.register = []

    @property
    def instructions(self):
        pass


    def load_program(self, program: Program):
        self.program = None

    def generate_constraints(self) -> Iterator[Identity]:

        for opcode, arguments in self.program:
            yield self.opcode[instruction](arguments*)

