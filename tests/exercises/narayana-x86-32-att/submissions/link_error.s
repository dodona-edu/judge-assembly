narayana:
    pushl 4(%esp)
    call fibonacci
    addl $4, %esp
    ret
