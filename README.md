# Parse trees for regular expressions in O(n m) time

This is my MSc thesis for Oscar Nierstrasz at the university of Bern. It
describes a parsing algorithm for regular expression that not only gives one
match for each capture group, but in fact all of them (that are consistent with
each other).

## Abstract
Regular expressions naturally and intuitively define parse trees that describe
the text that they’re parsing. We describe a technique for building up the
complete parse tree resulting from matching a text against a regular expression.
In standard tagged deterministic finite-state automaton (TDFA) matching, all
paths through the non-deterministic finite-state automaton (NFA) are walked
simultaneously, in different co-routines, where inside each co-routine, it is
fully known when which capture group was entered or left. We extend this model
to keep track of not just the last opening and closing of capture groups, but
all of them. We do this by storing in every co-routine a history of the all
groups using the flyweight pattern. Thus, we log enough information during
parsing to build up the complete parse tree after matching in a single pass,
making it possible to use our algorithm with strings exceeding the machine’s
memory.  This is achieved in worst case time O(m n), providing full parse trees
with only constant slowdown compared to matching.
