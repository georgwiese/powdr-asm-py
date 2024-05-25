import re
from typing import List, Dict
from pyparsing import Word, alphas, nums, Literal, oneOf, Group, ZeroOrMore, Forward, Suppress
Program = List[Dict]


def _parse_expression(expression: str):
    tokens = re.split(r'\s*\+\s*', expression)
    inputs = []
    for token in tokens:
        if token.isalpha():
            inputs.append([("A", 1)])  # Assuming all variables are 'A' with a weight of 1 for simplicity
        else:
            inputs.append([("CONST", int(token))])
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




