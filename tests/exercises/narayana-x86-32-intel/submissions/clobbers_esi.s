narayana:
    mov ecx, [esp + 4]      # iterations left: n - 2
    sub ecx, 2
    mov edx, 1              # N(k - 2)
    mov esi, 1              # N(k - 1), without saving esi first
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
    ret
