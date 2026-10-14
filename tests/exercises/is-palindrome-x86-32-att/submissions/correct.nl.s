is_palindrome:
    movl 4(%esp), %ecx      # first character
    movl %ecx, %edx
.Lend:
    cmpb $0, (%edx)
    je .Lfound
    incl %edx
    jmp .Lend
.Lfound:
    decl %edx               # last character
.Lloop:
    cmpl %edx, %ecx
    jae .Lyes
    movb (%ecx), %al
    cmpb (%edx), %al
    jne .Lno
    incl %ecx
    decl %edx
    jmp .Lloop
.Lyes:
    movl $1, %eax
    ret
.Lno:
    movl $0, %eax
    ret
