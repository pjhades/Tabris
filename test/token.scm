(define (fact n)
  (if (< n 2)
	1
	(* n (fact (- n 1)))))

(define (foo x); first "line"
  (list x
		'(+ 5 'x)
		"this is not ' quote" ;)
		)); end!





       (foo ; now let's take some evil input
	   "this is a string spans
  multiple 
                 lines"
	   '          

''''    ''(


	   this is the symbol quote)

	   )


	   '()


(incomplete 'ok)


'one'two'three

"string""after""another""
final one is multiline"



