narayana:
    mov w1, #0
    stp x29, x30, [sp, -8]!
    mov x29, sp
    bl narayana_hulp
    ldp x29, x30, [sp], 8
    mov w0, w1
    ret
narayana_hulp:
    cmp w0, #2
    b.gt L4
    add w1, w1, #1
    ret
L4:
    stp x29, x30, [sp, -8]!
    mov x29, sp
    sub w0, w0, #1
    bl narayana_hulp
    sub w0, w0, #2
    bl narayana_hulp
    ldp x29, x30, [sp], 8
    add w0, w0, #3
    ret