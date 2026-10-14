narayana:
    sub w0, w0, #2          // iterations left: n - 2
    mov w1, #1              // N(k - 2)
    mov w2, #1              // N(k - 1)
    mov w3, #1              // N(k)
.Lloop:
    cmp w0, #0
    b.le .Ldone
    add w19, w3, w1         // N(k + 1), without saving x19 first
    mov w1, w2
    mov w2, w3
    mov w3, w19
    sub w0, w0, #1
    b .Lloop
.Ldone:
    mov w0, w3
    ret
