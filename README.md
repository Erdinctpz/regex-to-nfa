# Regular Expression to NFA Converter
This project is a tool that converts a regular expression provided by the user into a Non-deterministic Finite Automaton (NFA.)

First, the regular expression is converted into postfix notation. Then, the postfix regular expression is converted into an NFA using the Thompson construction algorithm.




## Symbols That Can Be Used in Regular Expressions:

1. '+': Union – Selects between two subexpressions.

2. '*': Kleene Star – Allows a subexpression to repeat zero or more times.

3. '.': Concatenation – Joins two subexpressions in sequence.

4. '()': Group – Groups subexpressions and determines the order of operations.

### Note
Since each substate is combined with an 'ε', additional states may be created, leading to an increase in the number of states. 