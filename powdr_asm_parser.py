import re
from typing import List, Dict
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


def parse_powdr_assembly_code(input_text: str) -> Program:
    """
    :param input_text:
    # Example usage
        input_text = function main {
                 A <=X= A + 3;
                 A, B <== incr(A + 3);
                 A <== decr(A);
                 mstore 4, 5;
                 return;
        }
    :return: Program which is a list of instructions
    """
    # Split input into lines and strip unnecessary whitespace
    lines = [line.strip() for line in input_text.splitlines() if line.strip()]

    # Initialize an empty program list
    program = []

    # Define grammar for parsing expressions


    variable = Group(Word(alphas))("variable")
    constant = Group(Word(nums))("constant")
    operand = variable | constant
    assignment_register = Group(Word(alphas))("assignment_register")
    mult = Literal("*")
    plus = Literal("+")
    minus = Literal("-")
    operator = mult | plus | minus
    expression_token = operator | operand
    expression = Group(OneOrMore(expression_token))("expression")

    assignment = Group(variable + "<=" + assignment_register + "=" + expression + ";")("assignment")

    instruction = Group(Word(alphas))("instruction")
    arguments = Optional(expression) + ZeroOrMore("," + expression)
    instruction_with_one_or_more_outputs = Group(variable + ZeroOrMore("," + variable) + "<==" + instruction + "(" + arguments + ");")("instruction_with_one_or_more_outputs")

    instruction_with_no_outputs = Group(instruction + arguments + ";")("instruction_with_no_outputs")

    instruction_with_no_inputs_and_no_outputs = Group(instruction + ";")("instruction_with_no_inputs_and_no_outputs")



    instruction_line = Forward()
    instruction_line <<= assignment | instruction_with_one_or_more_outputs | instruction_with_no_outputs | instruction_with_no_inputs_and_no_outputs

    for line in lines[1:]:
        parse_result = instruction_line.parseString(line, parseAll=True)
        if parse_result.assignment:
            program.append({
                        "inputs": parse_result.assignment.expression,
                        "instruction": "X",
                        "outputs": []
            })

    ## Regular expressions for matching different parts of the instructions
    #assign_regex = re.compile(r"(\w+)\s*<=X=\s*(.+);")
    #incr_regex = re.compile(r"(\w+)\s*<==\s*incr\((.+)\);")
    #decr_regex = re.compile(r"(\w+)\s*<==\s*decr\((.+)\);")
    #return_regex = re.compile(r"return;")
#
#
    #    if match := assign_regex.match(line):
    #        output, expression = match.groups()
    #        inputs = parse_expression(expression)
    #        program.append({
    #            "inputs": inputs,
    #            "instruction": "X",
    #            "outputs": [output]
    #        })
    #    elif match := incr_regex.match(line):
    #        output, expression = match.groups()
    #        inputs = parse_expression(expression)
    #        program.append({
    #            "inputs": inputs,
    #            "instruction": "incr",
    #            "outputs": [output]
    #        })
    #    elif match := decr_regex.match(line):
    #        output, expression = match.groups()
    #        inputs = parse_expression(expression)
    #        program.append({
    #            "inputs": inputs,
    #            "instruction": "decr",
    #            "outputs": [output]
    #        })
    #    elif return_regex.match(line):
    #        program.append({
    #            "inputs": [],
    #            "instruction": "_return",
    #            "outputs": []
    #        })

    return program




