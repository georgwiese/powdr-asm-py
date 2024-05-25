import pytest
from powdr_asm_parser import parse_powdr_assembly_code


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