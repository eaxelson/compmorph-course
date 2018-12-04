# Morphological generator:
# - input: cat+N+Sg+Poss
# - output: cat's

# Construct state by state and transition by transition.
# Classes HfstIterableTransducer and HfstTransition can be used for this.
# We also need the special symbol EPSILON.
# This is not the easiest way to do this, but demonstrates the very low-level
# functions that exist in the HFST API.

from hfst_dev import HfstIterableTransducer, HfstTransition, EPSILON

tr = HfstIterableTransducer()  # the transducer initially has one state, numbered zero, that is not final
s = tr.add_state()             # state number one is created
tr.add_transition(s-1, HfstTransition(s, 'c', 'c', 0))  # add transition from state 0 to 1 with input symbol c and output symbol c with no weight
s = tr.add_state()             # state number two is created...
tr.add_transition(s-1, HfstTransition(s, 'a', 'a', 0))
s = tr.add_state()
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

# Use Xerox-style regular expressions.
# They are explained in [ADD_LINK].
# The input and output still need to be manually tokenized,
# i.e. symbols must be separated by spaces.
# Also note that some special symbols must be preceded by a percent sign
# so that they will be interpreted literally.

from hfst_dev import regex

generator = regex("c a t %+N:0 %+Sg:0 %+Poss:'s")
print(generator.lookup('cat+N+Sg+Poss'))

# Also possible via cross-product (alignment of input and output tokens cannot be controlled)

generator = regex("[c a t %+N %+Sg %+Poss] .x. [c a t ' s]")
print(generator.lookup('cat+N+Sg+Poss'))

# The regexp parser is a powerful tool, but for generating morphologies, there is an easier way.

# LexC formalism is the easiest way to handle this. It is explained in [ADD_LINK].
# It requires some work to learn but
# - multicharacter symbols need to declared only once in the beginning of the script
# - no need to tokenize strings manually
# - lexical entries and morphological processes are easy to separate in so called continuation lexica

from hfst_dev import compile_lexc_script

generator = compile_lexc_script(
"""
Multichar_Symbols
	+N	! Noun tag
        +Sg	! Singular
        +Pl	! Plural
 	+Poss	! Possessive form

LEXICON Root
	Nouns ; ! No input, no output

!
! NOUNS start here
!

LEXICON Nouns

cat	N ;
dog	N ;

church	  N_s ;
kiss	  N_s ;

beauty:beaut	N_y ;
sky:sk		N_y ;


! The noun lexica N and Num are used for stems without any alternation

LEXICON N
+N:0	Num ;

LEXICON Num
+Sg:0	PossWithS ;
+Pl:s	PossWithoutS ;

! The noun lexica N_s and Num_s are used for stems that end in a sibilant
! and need an extra inserted "e"

LEXICON N_s
+N:0	Num_s ;

LEXICON Num_s
+Sg:0	PossWithS ;
+Pl:es	PossWithoutS ;

! The noun lexica N_y and Num_y are used for stems with "y" -> "ie" alternation

LEXICON N_y
+N:0	Num_y ;

LEXICON Num_y
+Sg:y	PossWithS ;
+Pl:ies	PossWithoutS ;

! Possessive endings: usually the singular is 's and the plural is '

LEXICON PossWithS
+Poss:'s     # ;
	     # ; ! No ending: no input, no output

LEXICON PossWithoutS
+Poss:'	     # ;
	     # ; ! No ending: no input, no output

END
"""
)

# generator.lookup_optimize()
print(generator.lookup('sky+N+Pl'))
