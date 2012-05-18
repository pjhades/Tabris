(define (Hanoi n)
  (letrec ((move-them
           (lambda (n from to helper)
             (cond ((<= n 0) 'nothing-to-move)
                   ((= n 1) 1)
                   (else 
                     (+ (move-them (- n 1) from helper to)
                        1
                        (move-them (- n 1) helper to from)))))))
    (move-them n 1 2 3)))

(define (range start end step)
  (if (>= start end)
      '()
      (cons start (range (+ start step) end step))))

(define (calc-hanoi seq)
  (if (null? seq)
      (newline)
      (begin
        (display "Hanoi " (car seq) "is: " (Hanoi (car seq)))
        (newline)
        (calc-hanoi (cdr seq)))))

(calc-hanoi (range 1 10 1))
