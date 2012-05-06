(let ((a 1)
      (b 1))
  (+ a b))

(letrec ((odd? (lambda (n)
                 (if (= n 0)
                     #f
                     (even? (- n 1)))))
         (even? (lambda (n)
                  (if (= n 0)
                      #t
                      (odd? (- n 1))))))
  (odd? 1000))
