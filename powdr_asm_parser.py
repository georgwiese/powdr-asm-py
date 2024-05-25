import re
from typing import List, Dict
from pyparsing import Word, alphas, nums, Literal, oneOf, Group, ZeroOrMore, Forward, Suppress, Optional, Combine, OneOrMore
Program = List[Dict]


def parse_expression(expression):
    # Define grammar for parsing expressions
    variable = Word(alphas)
    constant = Word(nums)
    operand = variable | constant

    mult = Literal("*")
    plus = Literal("+")
    minus = Literal("-")
    plus_minus = Group(plus | minus)("sign")

    expr = Forward()
    term = Group(operand("first_operand") + Optional(Group((mult + operand("second_operand")))))
    expr <<= OneOrMore(Optional(plus_minus) + term) + ZeroOrMore(plus_minus + term)

    parse_result = expr.parseString(expression, parseAll=True)

    inputs = []

    if multiplication := parse_result.mult:
        if multiplication.variable[0] == "-":
            factor = -multiplication.factor
        else:
            factor = multiplication.factor
        inputs.append(
            (multiplication.variable, factor)
        )

    if shift_group := parse_result.shift:
        inputs.append(
            ("CONST", )
        )

    #if single_variable := variable.parseString(expression, parseAll=)

    #parsed_expr = term.parseString(expression, parseAll=True)


    for term in parsed_expr[0]:
        if len(term) == 1:
            # Single operand
            token = term[0]
            if token.isalpha():
                inputs.append((token, 1))  # Assuming variables are 'A', 'B', etc. with weight 1
            else:
                inputs.append(("CONST", int(token)))
        else:
            pass
    return inputs


def parse_powdr_assembly_code(input_text: str) -> Program:
    """
    :param input_text:
    # Example usage
        input_text = function main {
                 A <=X= A + 3;
                 A <== incr(A + 3);
                 A <== decr(A);
                 return;
        }
    :return: Program which is a list of instructions
    """
    # Split input into lines and strip unnecessary whitespace
    lines = [line.strip() for line in input_text.splitlines() if line.strip()]

    # Initialize an empty program list
    program = []

    # Regular expressions for matching different parts of the instructions
    assign_regex = re.compile(r"(\w+)\s*<=X=\s*(.+);")
    incr_regex = re.compile(r"(\w+)\s*<==\s*incr\((.+)\);")
    decr_regex = re.compile(r"(\w+)\s*<==\s*decr\((.+)\);")
    return_regex = re.compile(r"return;")

    for line in lines:
        if match := assign_regex.match(line):
            output, expression = match.groups()
            inputs = _parse_expression(expression)
            program.append({
                "inputs": inputs,
                "instruction": "X",
                "outputs": [output]
            })
        elif match := incr_regex.match(line):
            output, expression = match.groups()
            inputs = _parse_expression(expression)
            program.append({
                "inputs": inputs,
                "instruction": "incr",
                "outputs": [output]
            })
        elif match := decr_regex.match(line):
            output, expression = match.groups()
            inputs = _parse_expression(expression)
            program.append({
                "inputs": inputs,
                "instruction": "decr",
                "outputs": [output]
            })
        elif return_regex.match(line):
            program.append({
                "inputs": [],
                "instruction": "_return",
                "outputs": []
            })

    return program




