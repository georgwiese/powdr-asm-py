from typing import Iterator

class AsignmentRegister:
    """
    Has const witness column
    """
    pass


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

    @instruction
    def _return(self) -> Iterator[Identity]:
        """
        fills the instructions until the end
        :return:
        """
        yield self.pc.n == self.pc


    def load_program(self, program: Program):
        self.program = None

    def generate_constraints(self) -> Iterator[Identity]:



        for opcode, arguments in self.program:
            yield self.opcode[instruction](arguments*)

