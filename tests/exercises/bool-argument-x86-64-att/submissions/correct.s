choose:
    movl %edx, %eax         # b
    testl %edi, %edi
    cmovnel %esi, %eax      # a if the flag is set
    ret
