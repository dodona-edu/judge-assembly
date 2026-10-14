narayana:
    movl 4(%esp), %ecx      # iterations left: n - 2
    subl $2, %ecx
    movl $1, %edx           # N(k - 2)
    movl $1, %ebp           # N(k - 1), without saving %ebp first
    movl $1, %eax           # N(k)
.Lloop:
    cmpl $0, %ecx
    jle .Ldone
    addl %eax, %edx         # N(k + 1) = N(k) + N(k - 2)
    xchgl %edx, %ebp
    xchgl %ebp, %eax
    decl %ecx
    jmp .Lloop
.Ldone:
    ret
