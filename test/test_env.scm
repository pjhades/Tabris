(define (addx x)
	(lambda (n)
		(+ n x)))

(define f (addx 10))

(f 123)
((addx 1) 99)
