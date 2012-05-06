(define (fact n)
  (if (< n 2)
      1
      (* n (fact (- n 1)))))

(define (fact-iter n r)
  (if (< n 2)
      r
      (fact-iter (- n 1) (* n r))))

(fact 10)
(fact-iter 10 1)
