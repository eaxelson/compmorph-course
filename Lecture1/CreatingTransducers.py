# # Creating transducers from scratch
#
# ## Xerox-style regular expressions.
#
# The regexp syntax is explained [here](https://github.com/hfst/python-hfst-4.0/wiki/Regular-Expression-Operators).
#
# ## Set theory for finite-state networks
#
# Networks for the empty language and the empty-string language created
# directly with special functions, regular expressions, and from scratch:

from hfst_dev import empty_fst, epsilon_fst, regex, HfstIterableTransducer

# ready-made functions for empty and empty-string languages/relations:
empty1 = empty_fst()
epsilon1 = epsilon_fst()

# same with regexps that denote the languages (note that there are more than one possible solution, basically amn infinite number)
empty20 = regex('0 - 0')
empty21 = regex('~[?*]')

epsilon20 = regex('0')
epsilon21 = regex('[]')

# same with transducers that the regexps will compile into
empty3 = HfstIterableTransducer() # one initial, non-final state
epsilon3 = HfstIterableTransducer()
epsilon3.set_final_weight(0, 0) # make the initial state final

# The brackets [ and ] are used for grouping regular expressions.
# For example  a b | c is the same as language {"ab","c"} and a [ b | c ] the same as {"ab","ac"} (concatenation has higher precedence than union).
#
# ```
# [ A | B ] denotes the union of the two languages A and B ("or"-operation)
# [ A & B ] denotes the intersection ("and"-operation)
# [ A - B ] denotes the subtraction of B from A
# [ A B ] denotes the concatenation
# [ A .o. B ] denotes the concatenation
# A.u denotes the upper (i.e. input) projection
# A.l denotes the lower (o.e. output) projection
# ```
# 
# A more comprehensive list of operators and special symbols:
#
# ```
# 0    the epsilon
# \?    any token
# %    escape character
# { }  concatenate non-multicharacter symbols
# " "  quote symbol
# :    pair separator
# ::   weight
#
# [ ]  group expression
# ~    complement
# \    term complement
# &    intersection
# -    minus
# $.   contains once
# $?   contains optionally
# $    contains once or more
# ( )  optionality
# +    Kleene plus
# *    Kleene star
# /    ignoring
# |    union
# <>   shuffle
# <    before
# >    after
# .o.  composition
# .x.  cross product
# ^n,k catenate from n to k times, inclusive
# ^>n  catenate more than n times
# ^>n  catenate less than n times
# ^n   catenate n times
# .r   reverse
# .i   invert
# .u   input side
# .l   output side
# ;    end of expression
# !    starts a comment until end of line
# #    starts a comment until end of line
# .#.  word boundary symbol in replacements, restrictions
# ```


# We create a transducer that maps "cat+N+Sg+Poss" into "cat's".
# In LexC, we could list the set of symbols, but now we must tokenize manually,
# i.e. symbols must be separated by spaces. Also note that some special symbols
# must be preceded by a percent sign so that they will be interpreted literally.

from hfst_dev import regex

generator = regex("c a t %+N:0 %+Sg:0 %+Poss:'s")
print(generator.lookup('cat+N+Sg+Poss'))

# This is also possible via cross-product (but alignment of input and output tokens cannot be controlled):

generator = regex("[c a t %+N %+Sg %+Poss] .x. [c a t ' s]")
print(generator.lookup('cat+N+Sg+Poss'))


# ## Constructing transducers state by state and transition by transition
#
# Classes HfstIterableTransducer and HfstTransition can be used for this.
# We also need the special symbol EPSILON.

from hfst_dev import HfstIterableTransducer, HfstTransition, EPSILON

tr = HfstIterableTransducer()  # the transducer initially has one state, numbered zero, that is not final
s = tr.add_state()             # state number one is created...
tr.add_transition(s-1, HfstTransition(s, 'c', 'c', 0))  # add transition from state 0 to 1 with input symbol c and output symbol c with no weight
s = tr.add_state()             # state number two is created...
tr.add_transition(s-1, HfstTransition(s, 'a', 'a', 0))
s = tr.add_state()             # and so on...
tr.add_transition(s-1, HfstTransition(s, 't', 't', 0))
s = tr.add_state()
tr.add_transition(s-1, HfstTransition(s, '+N', EPSILON, 0))
s = tr.add_state()
tr.add_transition(s-1, HfstTransition(s, '+Sg', EPSILON, 0))
s = tr.add_state()
tr.add_transition(s-1, HfstTransition(s, '+Poss', "'s", 0))
tr.set_final_weight(s, 0)      # make the last state final with zero weight

# Convert to HfstTransducer for lookup. HfstIterableTransducer is very limited and
# mostly intended for constructing transducers from scratch and iterating through their
# states and transitions.

from hfst_dev import HfstTransducer

generator = HfstTransducer(tr)
print(generator.lookup('cat+N+Sg+Poss'))
