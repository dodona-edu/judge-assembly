narayana:
	movl	4(%esp), %edi
	movl	$0, %eax
	call	narayana_hulp
	ret
narayana_hulp:
	cmpl	$2, %edi
	jg	.L4
	incl	%eax
	ret
.L4:
	decl	%edi
	call	narayana_hulp
	subl	$2, %edi
	call	narayana_hulp
	addl	$3, %edi
	ret
	