narayana:
    mov edi, dword ptr [esp+4]
    mov eax, 0
    call narayana_hulp
    ret
narayana_hulp:
    cmp edi, 2
    jg  L4
    inc eax
    ret
L4:
    dec edi
    call narayana_hulp
    sub edi, 2
    call narayana_hulp
    add edi, 3
    ret
