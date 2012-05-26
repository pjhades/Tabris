(define (filter pred seq)
  (cond ((null? seq) '())
        ((pred (car seq)) 
         (cons (car seq) (filter pred (cdr seq))))
        (else
         (filter pred (cdr seq)))))

(define (qsort seq)
  (cond ((null? seq) '())
        (else 
          (let* ((pivot (car seq)) 
                 (less (filter (lambda (x) 
                                 (<= x pivot)) 
                               (cdr seq))) 
                 (greater (filter (lambda (x) 
                                    (> x pivot)) 
                                  (cdr seq)))) 
            (append (qsort less)
                    (list pivot)
                    (qsort greater))))))

(qsort '(1 6 3 9 7 7 1 2 5 6 -1 -65 190 14))
