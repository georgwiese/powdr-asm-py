import pytest
from powdr_asm_parser import parse_powdr_assembly_code, parse_expression


@pytest.mark.parametrize("expression, expected_output", [
    ("+A + 3", [("A", 1), ("CONST", 3)]),
    ("+B * 6 + 1", [("B", 6), ("CONST", 1)]),
    ("+5 + 10", [("CONST", 5), ("CONST", 10)]),
    ("-A", [("A", -1)]),
    ("-2 * A + 1", [("A", -2), ("CONST", 1)])
])
def test_parse_expression(expression, expected_output):
    assert parse_expression(expression) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    (
            """function main {
                 A <=X= A + 3;
                 A <== incr(A + 3);
                 A <== decr(A);
                 return;
            }""",
            [
                {
                    "inputs": [[("A", 1), ("CONST", 3)]],
                    "instruction": "X",
                    "outputs": ["A"]
                },
                {
                    "inputs": [[("A", 1), ("CONST", 3)]],
                    "instruction": "incr",
                    "outputs": ["A"]
                },
                {
                    "inputs": [[("A", 1)]],
                    "instruction": "decr",
                    "outputs": ["A"]
                },
                {
                    "inputs": [],
                    "instruction": "_return",
                    "outputs": []
                }
            ]
    ),
    (
            """function main {
                 A <=X= 5 + 10;
                 A <== incr(5 + 10);
                 A <== decr(A);
                 return;
            }""",
            [
                {
                    "inputs": [[("CONST", 5), ("CONST", 10)]],
                    "instruction": "X",
                    "outputs": ["A"]
                },
                {
                    "inputs": [[("CONST", 5), ("CONST", 10)]],
                    "instruction": "incr",
                    "outputs": ["A"]
                },
                {
                    "inputs": [[("A", 1)]],
                    "instruction": "decr",
                    "outputs": ["A"]
                },
                {
                    "inputs": [],
                    "instruction": "_return",
                    "outputs": []
                }
            ]
    ),
    (
            """function main {
                 A <=X= A + 1;
                 return;
            }""",
            [
                {
                    "inputs": [[("A", 1), ("CONST", 1)]],
                    "instruction": "X",
                    "outputs": ["A"]
                },
                {
                    "inputs": [],
                    "instruction": "_return",
                    "outputs": []
                }
            ]
    ),
    (
            """function main {
                 return;
            }""",
            [
                {
                    "inputs": [],
                    "instruction": "_return",
                    "outputs": []
                }
            ]
    ),
    (
            """function main {
                 A <=X= 42;
                 A <== incr(42);
                 A <== decr(A);
                 return;
            }""",
            [
                {
                    "inputs": [[("CONST", 42)]],
                    "instruction": "X",
                    "outputs": ["A"]
                },
                {
                    "inputs": [[("CONST", 42)]],
                    "instruction": "incr",
                    "outputs": ["A"]
                },
                {
                    "inputs": [[("A", 1)]],
                    "instruction": "decr",
                    "outputs": ["A"]
                },
                {
                    "inputs": [],
                    "instruction": "_return",
                    "outputs": []
                }
            ]
    )
])
def test_parse_assembly_code(input_text, expected_output):
    assert parse_powdr_assembly_code(input_text) == expected_output