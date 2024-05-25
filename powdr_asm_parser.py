import re
from typing import List, Dict
import re
from asm_to_pil import Statement
from pyparsing import Word, alphas, nums, Literal, oneOf, Group, ZeroOrMore, Forward, Suppress, Optional, Combine, OneOrMore
Program = List[Dict]


def parse_expression(expression):

    if expression[0] != "+" and expression[0] != "-":
        expression = "+" + expression

    # Define grammar for parsing expressions
    variable = Group(Word(alphas))("variable")
    constant = Group(Word(nums))("constant")
    operand = variable | constant

    mult = Literal("*")
    plus = Literal("+")
    minus = Literal("-")
    plus_minus = Group(plus | minus)("sign")

    expr = Forward()
    summands = Group(plus_minus("sign") + operand("first_factor") + Optional(Group((mult + operand("second_factor")))))
    expr <<= OneOrMore(summands)

    parse_result = expr.parseString(expression, parseAll=True)

    inputs = []

    for term in parse_result:
        if len(term) == 2:
            if term.sign[0] == "+":
                sign = 1
            else:
                sign = -1

            if term.variable:

                inputs.append((term.variable[0], sign))
            else:
                inputs.append(
                    ("CONST", sign * int(term.constant[0]))
                )
        elif len(term) == 3:
            if term.sign[0] == "+":
                sign = 1
            else:
                sign = -1
            if term.variable:
                inputs.append(
                    (term.variable[0], sign * int(term[2].constant[0]))
                )
            else:
                inputs.append(
                    (term[2].variable[0], sign * int(term.constant[0]))
                )


    return inputs

def parse_assembly_line(line):
    # Remove all whitespace
    line = re.sub(r'\s+', '', line).rstrip(';')

    # Regular expressions to match different types of instructions and assignments
    assignment_pattern = re.compile(r'([\w_,]+)<==(.+)')
    instruction_pattern = re.compile(r'([\w_]+)\((.*)\)')

    # Initialize the result dictionary
    result = {
        'instruction': '',
        'outputs': [],
        'inputs': []
    }

    # Check for multi-assignment or single assignment
    assign_match = assignment_pattern.match(line)
    if assign_match:
        outputs, inputs = assign_match.groups()
        result['outputs'] = outputs.split(',')
        
        # Check if the inputs contain an instruction with parentheses
        instr_match = instruction_pattern.match(inputs)
        if instr_match:
            instruction, operands = instr_match.groups()
            result['instruction'] = instruction
            result['inputs'] = [parse_expression(o) for o in operands.split(',')]
        else:
            result['instruction'] = 'IN_0'
            result['inputs'] = [parse_expression(inputs)]
        return result

    # Check for standalone instructions with parentheses
    instr_match = instruction_pattern.match(line)
    if instr_match:
        instruction, operands = instr_match.groups()
        result['instruction'] = instruction
        result['inputs'] = [parse_expression(o) for o in operands.split(',')]
        return result

    # If no match, it's a standalone instruction like "return"
    result['instruction'] = line
    return result

def parse_assembly(program):
    result = []
    for line in program.split('\n'):
        if line and not re.sub(r'\s+', '', line).startswith("//"):
            parsed_line = parse_assembly_line(line)
            statement = Statement(parsed_line['instruction'], parsed_line['inputs'], parsed_line['outputs'])
            result.append(statement)
    return result