from main_processor import MainProcessor

class RiscVProcessor(MainProcessor):

    def __init__(self):
        super(RiscVProcessor, self).__init__()
        self.X_b4 = WitnessColumn()
        self.X = AssignmentRegister()
        self.XIsZero = WitnessColumn()

    def global_constraints(self):
        yield ...

    @instruction
    def branch_if_zero(self, x: AssignmentRegister, y: AssignmentRegister):


    @instruction
    def add(self, x: Argument, y: Argument, z: Output) -> Iterator[Identity]:
        yield z == x + y

