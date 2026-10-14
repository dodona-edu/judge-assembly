string_length:
    sub esp, 4
    mov dword ptr [esp], 0  # length, kept on the stack
.Lloop:
    mov edx, [esp + 8]      # s, reloaded every iteration
    mov ecx, [esp]
    cmp byte ptr [edx + ecx], 0
    je .Ldone
    inc dword ptr [esp]
    jmp .Lloop
.Ldone:
    mov eax, [esp]
    add esp, 4
    ret
