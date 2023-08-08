narayana:
    mov r1, #0
    add r13, #-4
    str r11, [r13]
    str r14, [r13, #4]
    mov r8, sp
    bl narayana_hulp
    ldr r11, [r13]
    ldr r14, [r13, #4]
    add r13, #4
    mov r0, r1
    bx lr
narayana_hulp:
    cmp r0, #2
    bgt L4
    add r1, r1, #1
    bx lr
L4:
    add r13, #-4
    str r11, [r13]
    str r14, [r13, #4]
    mov r11, sp
    sub r0, r0, #1
    bl narayana_hulp
    sub r0, r0, #2
    bl narayana_hulp
    ldr r11, [r13]
    ldr r14, [r13, #4]
    add r13, #4
    add r0, r0, #3
    bx lr