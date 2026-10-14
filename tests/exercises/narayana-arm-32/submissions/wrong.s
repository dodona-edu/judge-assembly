narayana:
    sub r0, r0, #2          @ iterations left: n - 2
    mov r1, #1              @ N(k - 2)
    mov r2, #1              @ N(k - 1)
    mov r3, #1              @ N(k)
.Lloop:
    cmp r0, #0
    ble .Ldone
    add r12, r3, r2         @ N(k + 1) = N(k) + N(k - 1)
    mov r1, r2
    mov r2, r3
    mov r3, r12
    sub r0, r0, #1
    b .Lloop
.Ldone:
    mov r0, r3
    bx lr
