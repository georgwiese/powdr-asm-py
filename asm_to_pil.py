from powdr import star, FixedColumn, WitnessColumn, PIL, Identity, generate_pil, NumberExpression
from typing import Callable, Dict, Generator, List, Optional, Tuple, Union

def read_name(assignment_register: str, register: str) -> str:
    return f"read_{assignment_register}_{register}"

def write_name(assignment_register: str, register: str) -> str:
    return f"write_{assignment_register}_{register}"

def transform_vm(registers, assignment_registers, instructions, program) -> PIL:

    # Generate instructions to read into assignment registers
    # Example: X == ((X_const + (read_X_PC * PC)) + (read_X_A * A))
    for assignment_register in assignment_registers:
        const_col = WitnessColumn(f"{assignment_register}_const")
        expr = const_col
        
        pc_flag = WitnessColumn(read_name(assignment_register, "PC"))
        pc_col = WitnessColumn("PC")
        expr = expr + pc_flag * pc_col
        
        for register in registers:
            flag = WitnessColumn(read_name(assignment_register, register))
            expr = expr + (flag * WitnessColumn(register))

        assignment_register_col = WitnessColumn(assignment_register)
        yield assignment_register_col == expr

    # Generate instructions to write from assignment registers
    # Example: A' = IS_FIRST' * (write_X_A * X + write_Y_A * Y + (1 - (write_X_A + write_Y_A)) * A);
    # TODO: Handle instructions that write to registers directly (e.g. _return!)
    for register in registers + ["PC"]:
        expr = NumberExpression(0)
        flag_sum = NumberExpression(0)
        for assignment_register in assignment_registers:
            flag = WitnessColumn(write_name(assignment_register, register))
            assignment_register_col = WitnessColumn(assignment_register)
            expr = expr + flag * assignment_register_col
            flag_sum = flag_sum + flag

        register_col = WitnessColumn(register)
        IS_FIRST = FixedColumn("IS_FIRST", [1] + star([0]))

        default_value = register_col + 1 if register == "PC" else register_col

        yield register_col.n == IS_FIRST * (expr + (1 - flag_sum) * default_value)
    
    # Generate conditional instruction constraints
    for instruction in instructions:
        _, _, constraints = instruction()
        instruction_flag = WitnessColumn(f"instr_{instruction.__name__}")
        for constraint in constraints:
            yield instruction_flag * (constraint.left - constraint.right) == 0

    # TODO Generate and insert program columns & PC lookup

