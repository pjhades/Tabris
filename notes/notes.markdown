Implementation Notes
----------------------------
## The flow
code -> [tokenizer] -> tokens -> [parser] -> S-expressions -> [compiler] -> instructions -> [vm] -> result

## Tokenizer
* Split the code with `" ' \n \t ; ( )` characters;
* Scan the input line of code, maintain the states:
    * string not end (decide if we are reading the text of a string)
	* comment not end (decide if the code till the `\n` should be ignored)
	* quote not end (decide if the current token is the quote text)
	* level of parenthesis (check if the code is end)
* Gather each token according to the above three flags;
* Annotate the type of each token.

## Parser
* Parse the token streams in a recursive descent way with 1 lookahead token (operate directly on the token stream, no lookahead buffer):
	* If we see a datum token, convert it to its actual type (e.g. token `#t` will be converted to Python `True`)
	* If we see a quotation mark, recursively parse the following S-expression, and then make the quotation `(quote xxx)`
	* If we see a left parenthesis `(`, consume the `(`, recursively parse the list, and consume the `)`

## Compiler
* Compile the S-expressions to virtual machine instructions;
* Labels of jump instructions:
	* A label generator produces unique labels
	* Resolve labels (recode the address and compute the offset between the source and destination of the jump) 
	  before passing the compiled code to the VM
* Find all `define`s in a sequence, bind the `define`ed variables to Python `None` in the runtime environment.
  If their actual values are not set when being accessed, runtime error will be reported. This enables the mutual
  recursion like `even?` and `odd?`.

## Virtual machine
* Only 4 registers:
	* `VAL`: value register, store the results or used as a temporary storage
	* `ARGS`: store arguments of a function call
	* `PC`: program counter
	* `ENV`: pointer to the runtime environment
* Toplevel bindings;
* A stack that holds activation records and other things.

## Activation records
* Record the state of the VM;
* The runtime environment;
* The code sequence;
* The return address.

## Closures
* Contains an enviroment and its body;
* Two flags:
	* `isvararg`: if it can accept a variable argument list, e.g. `(define (f . b) (length b))`
	* `isprim`: if it is a primitive function
* Call of closures:
	* Create an activation record on the stack of the virtual machine
	* Point `PC` register to the start of the closure body
	* Execute the instructions in the closure body
	* Pop the top activation record on the stack
	* Restore old VM state

## Tail calls
* Normall calls and tail calls are distinguished by the position of the calls;
* The evaluation of calls:
	* Evaluate the arguments, put them into the `ARGS` register
	* Evaluate the function
	* Invoke the closure object with `call` or `tailcall` instruction
* If a call is a normal call, original `ARGS` register will be pushed onto the stack, and popped after
  the call;
* If a call is a tail call, it will reuse the original `ARGS` since the content of the 
  current activation record will never be used again.

## Lexical addressing
* Compile-time enviroment contains only the literal names of variables;
* All reference of variables are converted to the lexical addresses, which consist of:
	* The number of enviroment frames we should go back across
	* The index of the variable in the destination environment frame
* The lexical addresses will be generated when compiling the code that are related to variable accesses;
* Runtime enviroment contains only the lexical addresses of variables, no names are used.

## Continuations
* Holds the stack of the VM;
* The `call/cc` function is implemented directly as VM instructions, which is equivalent to the Scheme code:

	 (define (call/cc func)    
	     (let ((cc (capture)))    
	         (func (lambda (value)    
	                   (restore cc)    
	                   value))))    


## Trampolines
* A method to simulate arbitrarily deep recursions;
* Not return the recursive call, but return a "thunk" object, which holds:
	* The function to call next
	* The arguments on which the function will be called
* Work well with CPS (Continuation-Passing Style);
* Used in the parser, compiler and some utility functions.

## Several refactors
* At first, the tokenizer was implemented by setting up a DFA to recognize the patterns of each token type. This is overkilling since
  the Scheme code is not very complicated. Just splitting the tokens with delimiters will be enough;
* Originally, the parser converts the token stream into nested Python lists, e.g. `(+ (f 2) 3)` would be converted to `['+', ['f', '2'], '3']`,
  and the evaluator simply scans the lists and evaluats the code with native Python recursion. Obviously, the stack cannot support too deep
  recursions, so trampoline is involved to solve this problem;
* The evaluator was once implemented as a direct "evaluator" as in Chapter 4 of SICP. Of course this is slow since if a function is called
  multiple times, it will be parsed and executed multiple times. So a compiler and a toy virtual machine is added, and only the compiled
  instructions will be executed multiple times now.

## Things to do
* Write it in C
* Build AST
* Compile bytecode
* Improve the performance of VM
