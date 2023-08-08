narayana:
    mov rax, 0
    call narayana_hulp
    ret
narayana_hulp:
    cmp rdi, 2
    jg L4
    inc rax
    ret
L4:
    dec rdi
    call narayana_hulp
    sub rdi, 2
    call narayana_hulp
    add rdi, 3
    ret
    