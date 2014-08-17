.global _start


_start:
adds x3, x3, _start
adds x2, x2, #10
cbz x3, S
adds x2, x2, #-100
S:
adds x2, x2, #-1
b.pl S
