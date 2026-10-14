narayana:
    subl $2, %edi           # iterations left: n - 2
    movl $1, %edx           # N(k - 2)
    movl $1, %ebp           # N(k - 1), without saving %rbp first
    movl $1, %eax           # N(k)
.Lloop:
    cmpl $0, %edi
    jle .Ldone
    addl %eax, %edx         # N(k + 1) = N(k) + N(k - 2)
    xchgl %edx, %ebp
    xchgl %ebp, %eax
    decl %edi
    jmp .Lloop
.Ldone:
    ret
