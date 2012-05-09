(cond (#f "you will never see this")
      ((= (+ 9 1) 10) "it equals ten")
      (else "you will never see this either"))

(cond (#f "you will never see this")
      ('(1 . 9) => (lambda (p) (+ (car p) (cdr p))))
      (else "you will never see this either"))
