// Writes some values to memory and then multiplies
// all nonzero values up to cell 9.

mstore(0, 2);
mstore(7, 4);
mstore(17, 22);

// A stores the current index
A <== 0;
// B stores the product
B <== 1;

branch_if_zero(A - 10, 11);
C <== mload(A);
branch_if_zero(C, 9);
B <== mul(B, C);
A <== A + 1;
jump(5);

// The result should be 8
assert_zero(B - 8);

return;