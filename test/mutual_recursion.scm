(define (even? n)
	(if (= n 0)
		#t
		(odd? (- n 1))))

(define (odd? n)
	(if (= n 0)
		#f
		(even? (- n 1))))

(odd? 1000)

;(define (test n)
;    (define (even? n)
;    	(if (= n 0)
;    		#t
;    		(odd? (- n 1))))
;    
;    (define (odd? n)
;    	(if (= n 0)
;    		#f
;    		(even? (- n 1))))
;    (odd? n))
;
;(test 123)
;
;(begin
;    (define (even? n)
;    	(if (= n 0)
;    		#t
;    		(odd? (- n 1))))
;    
;    (define (odd? n)
;    	(if (= n 0)
;    		#f
;    		(even? (- n 1))))
;    (odd? 51))
;
;(cond (#t (define (even? n)
;            (if (= n 0)
;                #t
;                (odd? (- n 1))))
;          (define (odd? n)
;            (if (= n 0)
;                #f
;                (even? (- n 1))))
;          (odd? 123))
;      (else 'never))
;
;(cond (#f 'never)
;      (else (define (even? n) 
;              (if (= n 0)
;                  #t
;                  (odd? (- n 1))))
;            (define (odd? n)
;              (if (= n 0)
;                  #f
;                  (even? (- n 1))))
;            (odd? 123)))
;
;(let ()
;  (define (even? n) 
;    (if (= n 0)
;        #t
;        (odd? (- n 1))))
;  (define (odd? n)
;    (if (= n 0)
;        #f
;        (even? (- n 1))))
;  (odd? 123))
;
;(let* ()
;  (define (even? n) 
;    (if (= n 0)
;        #t
;        (odd? (- n 1))))
;  (define (odd? n)
;    (if (= n 0)
;        #f
;        (even? (- n 1))))
;  (odd? 123))
;
;(letrec ()
;  (define (even? n) 
;    (if (= n 0)
;        #t
;        (odd? (- n 1))))
;  (define (odd? n)
;    (if (= n 0)
;        #f
;        (even? (- n 1))))
;  (odd? 123))
;
;(let foo ()
;  (define (even? n) 
;    (if (= n 0)
;        #t
;        (odd? (- n 1))))
;  (define (odd? n)
;    (if (= n 0)
;        #f
;        (even? (- n 1))))
;  (odd? 123))

