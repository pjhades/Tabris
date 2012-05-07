((lambda x (cdr x)) '(1 2 3 4))

((lambda (x . y) (cons x y)) 1 2 3 4 5)

((lambda (x y . z) (append z (list x y))) 'x 'y 1 2 3)
