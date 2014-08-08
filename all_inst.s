.global _start

_start:
ADD w1, w2, w3
ADDS w1, w2, w3
SUB w1, w2, w3
SUBS w1, w2, w3
ADR x2,_start 
ADRP x2, _start
ASR w1, w2, w3
AND w1, w2, w3
B _start
BR X2
BL _start
BLR x2
CBZ w2, _start
CMP w1, w2
LDP w1, w2, [sp], #12
LDR w1, [X1], #10
LDRSW x1, [x2], #10
LSL w1, w2, w3 
LSR w1, w2, w3 
MOV w1, w2
STP w1, w2, [x1], #12
STR w1, [x1], #24
BLE     ng+8
BL      subC
NOP 
