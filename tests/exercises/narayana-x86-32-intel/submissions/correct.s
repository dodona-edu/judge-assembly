narayana:
    push esi
    mov ecx, [esp + 8]      # iterations left: n - 2
    sub ecx, 2
    mov edx, 1              # N(k - 2)
    mov esi, 1              # N(k - 1)
    mov eax, 1              # N(k)
.Lloop:
    cmp ecx, 0
    jle .Ldone
    add edx, eax            # N(k + 1) = N(k) + N(k - 2)
    xchg edx, esi
    xchg esi, eax
    dec ecx
    jmp .Lloop
.Ldone:
    pop esi
    ret
