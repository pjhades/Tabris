(define counter 0)
(define cc 0)
(call/cc (lambda (c)
           (set! cc c)))
(set! counter (+ counter 1))
(cc "see this?")
