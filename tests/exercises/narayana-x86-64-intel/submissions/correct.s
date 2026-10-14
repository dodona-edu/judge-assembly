narayana:
    sub edi, 2              # iterations left: n - 2
    mov edx, 1              # N(k - 2)
    mov ecx, 1              # N(k - 1)
    mov eax, 1              # N(k)
.Lloop:
    cmp edi, 0
    jle .Ldone
    add edx, eax            # N(k + 1) = N(k) + N(k - 2)
    xchg edx, ecx
    xchg ecx, eax
    dec edi
    jmp .Lloop
.Ldone:
    ret
