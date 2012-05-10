; this is a tail call
(define (addup n sum)
  (if (= n 0)
      sum
      (addup (- n 1) (+ n sum))))

; this is NOT a tail call
(begin
    (addup 10 0))

; try test/mutural_recursion.scm
