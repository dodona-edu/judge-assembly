string_length:
    mov edx, [esp + 4]      # s
    xor eax, eax            # length
.Lloop:
    inc eax                 # counts the terminating zero too
    cmp byte ptr [edx + eax - 1], 0
    jne .Lloop
    ret
