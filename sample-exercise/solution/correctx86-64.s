narayana:
	movq $0, %rax
	call narayana_hulp
	ret
narayana_hulp:
	cmpq $2, %rdi
	jg .L4
	incq %rax
	ret
.L4:
	decq %rdi
	call narayana_hulp
	subq $2, %rdi
	call narayana_hulp
	addq $3, %rdi
	ret
	