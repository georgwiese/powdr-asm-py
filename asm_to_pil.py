from powdr import star, lookup, FixedColumn, Expression, WitnessColumn, PIL, Identity, generate_pil, NumberExpression
from typing import Callable, Dict, Generator, List, Optional, Tuple, Union

def read_name(assignment_register: str, register: str) -> str:
    return f"read_{assignment_register}_{register}"

def write_name(assignment_register: str, register: str) -> str:
    return f"write_{assignment_register}_{register}"

def is_reg_prime(expr: Expression, register_name: str) -> bool:
    if isinstance(expr, WitnessColumn):
        return expr.name == register_name and expr.is_next
    return False

def find_assignment(constraints: List[Identity], register_name: str) -> Optional[Expression]:
    assignment = None
    for constraint in constraints:
        if is_reg_prime(constraint.left, register_name):
            assignment = constraint.right
        elif is_reg_prime(constraint.right, register_name):
            assignment = constraint.left
    return assignment

def has_assignment(constraint: Identity, register_names: List[str]) -> bool:
    return any(is_reg_prime(constraint.left, register_name) or
               is_reg_prime(constraint.right, register_name)
               for register_name in register_names)
        

def transform_vm(registers, assignment_registers, instructions, program) -> PIL:

    # Generate instructions to read into assignment registers
    # Example: X == X_const + read_X_PC * PC + read_X_A * A + read_X_X_free * X_free
    for assignment_register in assignment_registers:
        const_col = WitnessColumn(f"{assignment_register}_const")
        expr = const_col
        
        for register in registers + ["PC"] + [f"{assignment_register}_free"]:
            flag = WitnessColumn(read_name(assignment_register, register))
            expr = expr + (flag * WitnessColumn(register))

        assignment_register_col = WitnessColumn(assignment_register)
        yield assignment_register_col == expr

    # Generate instructions to write from assignment registers
    # Example: A' = (1 - IS_FIRST') * (write_X_A * X + write_Y_A * Y + (1 - (write_X_A + write_Y_A)) * A);
    for register in registers + ["PC"]:
        expr = NumberExpression(0)
        flag_sum = NumberExpression(0)
        for assignment_register in assignment_registers:
            flag = WitnessColumn(write_name(assignment_register, register))
            assignment_register_col = WitnessColumn(assignment_register)
            expr = expr + flag * assignment_register_col
            flag_sum = flag_sum + flag

        # Handle instructions with constraints like: PC' = PC
        for instruction in instructions:
            _, _, constraints = instruction()
            assignment = find_assignment(constraints, register)
            if assignment is not None:
                expr = expr + WitnessColumn(f"instr_{instruction.__name__}") * assignment
                flag_sum = flag_sum + WitnessColumn(f"instr_{instruction.__name__}")

        register_col = WitnessColumn(register)
        IS_FIRST = FixedColumn("IS_FIRST", [1] + star([0]))

        default_value = register_col + 1 if register == "PC" else register_col

        yield register_col.n == (1 - IS_FIRST.n) * (expr + (1 - flag_sum) * default_value)
    
    # Generate conditional instruction constraints
    for instruction in instructions:
        _, _, constraints = instruction()
        instruction_flag = WitnessColumn(f"instr_{instruction.__name__}")
        for constraint in constraints:
            if not has_assignment(constraint, registers + ["PC"]):
                yield instruction_flag * (constraint.left - constraint.right) == 0

    # ================================== Generate program fixed columns
    # str -> (inputs, outputs)
    instruction_by_name = {instruction.__name__: (instruction()[0], instruction()[1])
                           for instruction in instructions}
    # For every assignment register, there is an "instruction" with the same input and output
    for assignment_register in assignment_registers:
        instruction_by_name[assignment_register] = ([assignment_register], [assignment_register])
    
    # Program columns: line number, instruction flags, read flags, write flags
    program_column_names = ["line"] + \
        [f"instr_{instruction.__name__}" for instruction in instructions] + \
        [read_name(assignment_register, register) for assignment_register in assignment_registers for register in registers + ["PC"] + [f"{assignment_register}_free"]] + \
        [write_name(assignment_register, register) for assignment_register in assignment_registers for register in registers + ["PC"]] + \
        [f"{assignment_register}_const" for assignment_register in assignment_registers]
    program_column_values = {name: [] for name in program_column_names}

    for i, statement in enumerate(program):
        # Example statement:
        # {
        #     "inputs": [[("A", 1), ("CONST", 3)]],
        #     "instruction": "incr",
        #     "outputs": ["A"]
        # }
        input_assignment_registers = instruction_by_name[statement["instruction"]][0]
        output_assignment_registers = instruction_by_name[statement["instruction"]][1]
        assert len(input_assignment_registers) == len(statement["inputs"])
        assert len(output_assignment_registers) == len(statement["outputs"])

        # Line number
        program_column_values["line"].append(i)

        # Instruction flags
        if statement['instruction'] not in assignment_registers:
            program_column_values[f"instr_{statement['instruction']}"].append(1)

        # Read flags and constants
        for assignment_register, inputs in zip(input_assignment_registers, statement["inputs"]):
            for register, factor in inputs:
                if register == "CONST":
                    program_column_values[f"{assignment_register}_const"].append(factor)
                else:
                    program_column_values[read_name(assignment_register, register)].append(factor)
        
        # Write flags
        for assignment_register, output, instruction in zip(output_assignment_registers, statement["outputs"], statement["instruction"]):
            program_column_values[write_name(assignment_register, output)].append(1)
            if instruction not in assignment_registers:
                program_column_values[read_name(assignment_register, f"{assignment_register}_free")].append(1)

        # All other columns should be padded with 0 to have the same length
        for column_values in program_column_values.values():
            if len(column_values) == i:
                column_values.append(0)

    program_columns = {name: FixedColumn(f"p_{name}", values + star([values[-1]]))
                       for name, values in program_column_values.items()}
    
    lhs = []
    rhs = []
    for program_column_name in program_column_names:
        lhs_column = WitnessColumn(program_column_name) if program_column_name != "line" else WitnessColumn("PC")
        lhs.append(lhs_column)
        rhs.append(program_columns[program_column_name])

    yield lookup(lhs, rhs)
