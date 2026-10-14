string_length:
    mov edx, [esp + 4]      # s
    xor eax, eax            # length
.Lloop:
    cmp byte ptr [edx + eax], 0
    je .Ldone
    inc eax
    jmp .Lloop
.Ldone:
    ret
