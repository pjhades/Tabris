;; search for the first occurrence
(define seen 0)

(define (search lst x)
  (call/cc (lambda (return)
             (cond ((null? lst) #f)
                   ((= (car lst) x) (return lst))
                   (else 
                     (set! seen (+ seen 1))
                     (search (cdr lst) x))))))

(search '(1 2 3 4 5 6 7) 3)
seen

; Yin-Yang puzzle
(let* ((yin ((lambda (x) (display "@") x)
             (call/cc (lambda (c) c))))
       (yang ((lambda (x) (display ".") x)
              (call/cc (lambda (c) c)))))
      (yin yang))
