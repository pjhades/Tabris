;; normal let
(let ((a 1)
      (b 1))
  (+ a b))

;; letrec mutural recursion
(letrec ((odd? (lambda (n)
                 (if (= n 0)
                     #f
                     (even? (- n 1)))))
         (even? (lambda (n)
                  (if (= n 0)
                      #t
                      (odd? (- n 1))))))
  (odd? 1000))

;; named let
(let foo ((a 10) 
          (b 0)) 
  (if (= a 0) 
      b 
      (foo (- a 1) 
           (+ a b))))
