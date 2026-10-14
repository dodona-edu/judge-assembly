narayana:
    subl $2, %edi           # iterations left: n - 2
    movl $1, %edx           # N(k - 2)
    movl $1, %ecx           # N(k - 1)
    movl $1, %eax           # N(k)
.Lloop:
    cmpl $0, %edi
    jle .Ldone
    movl %ecx, %edx
    addl %eax, %edx         # N(k + 1) = N(k) + N(k - 1)
    xchgl %edx, %ecx
    xchgl %ecx, %eax
    decl %edi
    jmp .Lloop
.Ldone:
    ret
