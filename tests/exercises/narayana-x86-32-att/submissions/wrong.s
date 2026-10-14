narayana:
    pushl %ebx
    movl 8(%esp), %ecx      # iterations left: n - 2
    subl $2, %ecx
    movl $1, %edx           # N(k - 2)
    movl $1, %ebx           # N(k - 1)
    movl $1, %eax           # N(k)
.Lloop:
    cmpl $0, %ecx
    jle .Ldone
    movl %ebx, %edx
    addl %eax, %edx         # N(k + 1) = N(k) + N(k - 1)
    xchgl %edx, %ebx
    xchgl %ebx, %eax
    decl %ecx
    jmp .Lloop
.Ldone:
    popl %ebx
    ret
