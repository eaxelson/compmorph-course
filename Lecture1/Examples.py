# # HFST - Helsinki Finite-State Technology
#
# The HFST toolkit is intended for processing natural language
# morphologies. The toolkit is demonstrated by wide-coverage
# implementations of a number of languages of varying morphological
# complexity. HFST is written mainly in C++, but there is a Python interface
# which is demonstrated on these notebooks.
#
# For installation of the HFST package for Python, see our [PyPI pages](https://pypi.org/project/hfst/).
#
# For more information about the interface, see our [Github wiki pages](https://github.com/hfst/python-hfst-4.0/wiki).
#
# This notebook page demonstrates morphological analysis and generation with HFST python API.
#
# ## 1. Using existing morphologies
#
# ### 1.1 Use standalone morphology packages (does not work yet)
#
# First import the morphology packages with:
#
# `pip import hfst-morphologies`
#
# start python and run:

from hfst_morphologies import english_bnc

english_bnc.analyze('cat')

# Expect the result:
#
# ```
# cat[N]+N        10.203125
# cat[V]+V+INF    18.454102
# ```

english_bnc.generate('cat[N]+N')

# Expect the result:
#
# ```
# cat     10.203125
# Cat     15.745117
# ```

english_bnc.tokenize('This is a cat.')

# Expect the result:
#
# `('This', 'is', 'a', 'cat', '.')`

# ### 1.2 Download the morphologies and process them with HFST
#
# For instance, download the English morphology from
# [Kielipankki](https://korp.csc.fi/download/hfst-morphologies/en/wn-bnc/hfst-en-morph-wn-bnc.zip) (The Language Bank of Finland),
# extract it and run python:

from hfst_dev import HfstTransducer

analyzer = HfstTransducer.read_from_file('hfst-en-morph-wn-bnc/english.hfst')
analyzer.lookup_optimize()
generator = HfstTransducer.read_from_file('hfst-en-morph-wn-bnc/hfst-english-installable/en-generation.hfst.ol')

print(analyzer.lookup('cat', output='text'))

# Output is:
#
# ```
# cat     cat[N]+N        10.203125
# cat     cat[V]+V+INF    18.454102
# ```

print(generator.lookup('cat[N]+N', output='text'))

# Output is:
#
# ```
# cat[N]+N        cat     10.203125
# cat[N]+N        Cat     15.745117
# ```

# ### 1.3 Compile the morphologies from source
#
# (TODO: the binaries are compiled with foma as hfst-xfst fails to produce the right result, so this will not work...)

from hfst_dev import compile_xfst_script

compile_xfst_script('hfst-en-morph-wn-bnc/src/english.script')
analyzer = HfstTransducer.read_from_file('hfst-en-morph-wn-bnc/src/english.hfst')
analyzer.lookup_optimize()
generator = HfstTransducer(analyzer)
generator.invert()
generator.minimize()

print(analyzer.lookup('cat', output='text'))
print(generator.lookup('cat[N]+N', output='text'))

# ## 2. Generating your own morphologies:
#
# HFST supports LexC, TwolC and XFST formalisms.
#
# A very simple example that generates plural, singular and possessive forms
# for a couple of English lexemes using LexC:

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

generator.lookup_optimize()
print(generator.lookup('sky+N+Pl'))
