// Writes some values to memory and then multiplies
// all nonzero values up to cell 9.

mstore(0, 2);
mstore(7, 4);
mstore(17, 22);

// A stores the current index
A <== 0;
// B stores the product
B <== 1;

// If index is 10, skip to the final assertion
branch_if_zero(A - 10, 11);
// Load the value at index A
C <== mload(A);
// Skip the next instruction if C is 0
branch_if_zero(C, 9);
// Multiply C into the accumulator
B <== mul(B, C);
// Increment the index
A <== A + 1;
// Jump back to the beginning of the loop
jump(5);

// The result should be 8
assert_zero(B - 8);

return;