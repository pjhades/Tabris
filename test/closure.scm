(define (addx x)
  (lambda (y)
    (+ y x)))

(define add5 (addx 5))
(define add10 (addx 10))

(add5 5)
(add5 9)
(add10 10)
(add10 -10)
