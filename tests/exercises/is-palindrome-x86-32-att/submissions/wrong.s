is_palindrome:
    movl 4(%esp), %ecx      # first character
    movl %ecx, %edx
.Lend:
    cmpb $0, (%edx)
    je .Lfound
    incl %edx
    jmp .Lend
.Lfound:
    decl %edx               # last character, the only one compared
    movb (%ecx), %al
    cmpb (%edx), %al
    jne .Lno
    movl $1, %eax
    ret
.Lno:
    movl $0, %eax
    ret
