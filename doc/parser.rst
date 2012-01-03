Tokenizer
--------------------
The tokenizer receives the input source code and produces
the tokens, omitting white blanks and comments. As the code
may span several lines, the tokenizer keeps track of some
states:
    1. we have seen an opening quote and are reading the
       content of a string
    2. we have seen a semicolon and are reading the content
       of the comment
    3. we have seen a single quote and are reading the
       quoted literals
With these states and the parentheses count, we can check 
if we need to read more code. After reading each piece of
code, the tokenizer splitts the code by the delimiters. If
the tokenizer does not need more code, get_tokens() can be
called to get the tokens we have found till now.

The Tokenizer class also has a method tokenize_single() to 
parse a single line of code.



Parser
---------------------
The parser takes as input a token list and constructs the 
syntax tree according to R^6RS datum syntax:
http://www.r6rs.org/final/html/r6rs/r6rs-Z-H-7.html#node_sec_4.3

The parser uses recursive descent parsing to build the syntax
tree. While building the tree, it converts the tokens to their
corresponding Scheme-type objects. The result of the syntax 
analysis is a Scheme list constructed by pairs, which is the same
as the meta-circular evaluator in SICP and this makes the data
and code undistinguishable, which is natural in Scheme.

Since Python does not provide tail call optimization, directly 
translating the evaluator in the text from Scheme into Python
will be limited by the stack depth. We employ trampoline style
as a trick to enable arbitrary depth of recursion.
