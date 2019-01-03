# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 1
#
# ## HFST - Helsinki Finite-State Technology
#
# The HFST toolkit is intended for processing natural language
# morphologies. The toolkit is demonstrated by wide-coverage
# implementations of a number of languages of varying morphological
# complexity. HFST is written mainly in C++, but there is a Python interface
# which is demonstrated on these notebooks.
#
# ## Prerequisites
#
# * Foundations of general linguistics
# * Basic knowledge on how to use a computer
# * Some programming experience is desirable
# * Knowledge of Natural Language Processing (NLP) is also a plus
#
# ## Course material
#
# If you want a book:
#
# * Kenneth R. Beesley and Lauri Karttunen: [Finite State Morphology](http://press.uchicago.edu/ucp/books/book/distributed/F/bo3613750.html), CSLI Publications, 2003.
# * Daniel Jurafsky and James H. Martin, Speech and Language Processing, Prentice Hall, second edition, 2009
#
# Links:
#
# * HFST [main page](https://hfst.github.io).
# * For installation of the HFST package for Python, see our [PyPI pages](https://pypi.org/project/hfst/).
# * For more information about the interface, see our [Github wiki pages](https://github.com/hfst/python-hfst-4.0/wiki).
#
# First, import the package and list its contents with `help`.

import hfst_dev
help(hfst_dev)

# Then, see for more information on some of the functions, e.g. `compile_lexc_file`.

help(hfst_dev.compile_lexc_file)

# Also print the version number of the package.

print(hfst_dev.__version__)

# ## Course overview
#
# | Lecture | Topics |
# | - | - |
# | 1 | (Introduction), lexc, xfst, replace rules |
# | 2 | Weighted finite state machines, (unsupervised morphology) |
# | 3 | Regular expressions, pronunciation lexicons, guessers, stemmers, twolc, two-level rules |
# | 4 | Flag diacritics, non-concatenative morphology |
# | 5 | Optimization of finite-state networks |
# | 6 | (Guest lecture) |
# | 7 | (Final project demos, technical presentetions) |

# ## 4. Hockett's models of morphology
#
# ### Word and Paradigm (W&P), Example: Finnish nouns
#
# | Numbers/Cases | Singular | Plural |
# | - | - | - |
# | *Nominative* | susi | sudet | 
# | *Genitive* | suden | susien, sutten |
# | *Partitive* | sutta | susia |
# | *Inessive* | sudessa | susissa |
# | *Elative* | sudesta | susista |
# | *Illative* | suteen | susiin |
# | *Adessive* | sudella | susilla |
# | *Ablative* | sudelta | susilta |
# | *Allative* | sudelle | susille |
# | *Essive* | sutena | susina |
# | *Translative* | sudeksi | susiksi |
# | *Instructive* | - | susin |
# | *Abessive* | sudetta | susitta |
# | *Comitative* | - | susine(en) |
#
# ### Item and Arrangement (I&A)
#
# * Morphemes and allomorphs
#   - "SUSI": susi, sude-, sute-, sut-, sus-
#   - Number:
#     * Singular: ∅ (or no morpheme at all: unmarked)
#     * Plural: -t, -i-, -j-
#   - Case:
#     * Genitive: -n, -en, -den, -tten
#     * Partitive: -a, -ä, -ta, -tä
#     * Etc.
# * The allomorphs occur in a specific distribution:
#   - E.g., sus- in all plural forms except nominative
#   - No allomorph is more "basic" than any other.
#
# ### Item and Process (I&P)
#
# We have roots or bases of morphemes and different processes apply to them.
#
# * Nominative: word final 'e' becomes 'i'; 't' in front of 'i' becomes 's' 🡒 "susi"
# * Genitive: add suffix '+n'; soften 't' to 'd' in closed syllable 🡒 "suden"
# * Etc.
#
# ### Corresponding HFST tools
#
# | Model/Tool | [compile_twolc_file](https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_twolc_file-inputfilename-outputfilename-kwargs) | [compile_lexc_file](https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_lexc_file-filename-kwargs) | [compile_xfst_file](https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_xfst_file-filename-kwargs) |
# | - | - | - | - |
# | Word & Paradigm |  | ✔ | ✔ |
# | Item & Arrangement |  | ✔ | ✔ |
# | Item & Process | ✔ |  | ✔ |
#
# See how they work. twolc:

help(hfst_dev.compile_twolc_file)

# lexc:

help(hfst_dev.compile_lexc_file)

# xfst:

help(hfst_dev.compile_xfst_file)

# interactive version of xfst:

help(hfst_dev.start_xfst)

# ## 5. Morphological generators and analyzers
#
# ### Morphological generator
#
# * Input (also called lexical form): `cat+N+Sg+Poss`
# * Output (also called surface form): `cat's`
# * The idea is to create a model that generalizes to new word forms.
#   - Wrong way: List all possible pairs of input and output in the lexeme:
#     * `cat+N+Sg` 🡒 cat
#     * `cat+N+Pl` 🡒 cats
#     * `cat+N+Sg+Poss` 🡒 cat's
#     * `cat+N+Pl+Poss` 🡒 cats'
#   - Right way: Model the inner regular morphological structure of words.
#     * This makes it possible to add a new lemma, such as `dog`, and the model knows how to inflect this word by analogy to the word `cat`.
#
# ### Morphological analyzer
#
# * Input (surface form): `cat's`
# * Output (lexical form): `cat+N+Sg+Poss`
# * An analyzer produces the opposite mapping compared to the generator:
#   - The input of the generator is the output of the analyzer.
#   - The output of the analyzer is the input of the generator.
# * An analyzer is very useful, for instance:
#   - when we want to parse natural language text syntactically
#   - when we want to _normalize_ text, such that we only care about the base form (lemma) of every word in the text; this is used, for instance, in _information_ _retrieval_.
#
# ## Some simple noun paradigms in English
#
# ```
# Paradigm: N
# cat +Sg (singular)
# cat|s +Pl (plural)
# cat|'s +Sg +Poss (singular possessive)
# cat|s' +Pl +Poss (plural possessive)
# Similarly: dog, pet, book, hill, fan
# ```
#
# ```
# Paradigm: N_s
# kiss +Sg (singular)
# kiss|es +Pl (plural)
# kiss|'s +Sg +Poss (singular possessive)
# kiss|es|' +Pl +Poss (plural possessive)
# Similarly: wish, mess, church, search, waitress
# ```
#
# Let's create a morphological generator and analyzer for this data.

# ## 6. A Finite-State Transducer that implements a morphological generator
#
# Below is a finite-state transducer (FST) for purely concatenative I&A English noun inflection
# for our simple example data.
# The yellow circles represent _states_ and the arrows represent _transitions_ between the states.
# State named _"Root"_ is the initial state and state named_"#"_ the final one.
# Above each transition, there is the input
# that the transition _consumes_ and the output that it _produces_, separated with a colon ":".
# The "ε:ε" signifies the _epsilon_ transition which is possible without consuming
# any input or producing any output.
# We will return to finite-state transducers in more detail in the next part.
#
# <img src="img/noun_inflection.png">

# ## 7. LexC code that represents this transducer
#
# ### 7.1 Define all symbols consisting of multiple characters
#
# ```
# Multichar_Symbols
#         +N      ! Noun tag
#         +Sg     ! Singular
#         +Pl     ! Plural
#         +Poss   ! Possessive form
#                 ! Another comment that is ignored by the compiler
# ```
#
# Anything between an exclamation mark and the end of a line
# is a comment. Comments are ignored by the lexc compiler.
# Use comments a lot!
# Your code will be clearer to yourself and to others.
#
# ### 7.2 Define the compulsory Root lexicon
#
# ```
# LEXICON Root
#         Nouns ; ! No input, no output
# ```
#
# This is equivalent to writing:
#
# ```
# LEXICON Root
# 0:0     Nouns ; ! Explicitly showing no input, no output
# ```
#
# This is further equivalent to writing:
#
# ```
# LEXICON Root
# 0       Nouns ; ! When the input and output are identical,
#                 ! you can type only the input side
# ```
#
# <img src="img/root_lexicon.png">
#
# ### 7.3 Define the Nouns lexicon
#
# ```
# !
# ! NOUNS start here
# !
#
# LEXICON Nouns
#
# cat     N ;
# dog     N ;
#
# church    N_s ;
# kiss      N_s ;
#
# beauty:beaut    N_y ;
# sky:sk          N_y ; 
#
# ```
# <img src="img/nouns_lexicon.png">
#
# ### 7.4 Continuation lexicons for the N paradigm
#
# ```
# ! The noun lexica N and Num are used for stems without
# ! any alternation
# 
# LEXICON N
# +N:0    Num ;
# 
# LEXICON Num
# +Sg:0   PossWithS ;
# +Pl:s   PossWithoutS ;
# ```
#
# <img src="img/n_paradigm.png">
#
# ### 7.5 Continuation lexicons for the N_s paradigm
#
# ```
# ! The noun lexica N_s and Num_s are used for stems that
# ! end in a sibilant and need an extra inserted "e"
#
# LEXICON N_s
# +N:0    Num_s ;
#
# LEXICON Num_s
# +Sg:0   PossWithS ;
# +Pl:es  PossWithoutS ;
# ```
#
# <img src="img/ns_paradigm.png">
#
# ### 7.6 Continuation lexicons for the N_y paradigm
#
# ```
# ! The noun lexica N_y and Num_y are used for stems with
# ! "y" -> "ie" alternation
#
# LEXICON N_y
# +N:0    Num_y ;
#
# LEXICON Num_y
# +Sg:y   PossWithS ;
# +Pl:ies PossWithoutS ;
# ```
#
# <img src="img/ny_paradigm.png">
#
# ### 7.7 Continuation lexicons for possessive ending
#
# ```
# ! Possessive endings: usually the singular is 's and 
# ! the plural is '
#
# LEXICON PossWithS
# +Poss:'s    # ; 
#             # ; ! No ending: no input/output 
# 
# LEXICON PossWithoutS 
# +Poss:'     # ;
#             # ; ! No ending: no input/output
#
# END
# ```
# <img src="img/poss_ending.png">
#
# Note that `END` signifies the end of lexc file. It must be included at the end of each LexC file.
#
# Finally, let's compile the LexC script into a transducer:

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

# We could also write the script to a file and then call `compile_lexc_file`.
#
# Test the transducer:

print(generator.lookup('sky+N+Pl'))

# expect the result `(('skies', 0.0),)`, i.e. output "skies" with a zero _weight_. We will return to weights in later lectures.
#
# Next, _invert_ the transducer to get an analyzer:

from hfst_dev import HfstTransducer
analyzer = HfstTransducer(generator)
analyzer.invert()
analyzer.minimize()

print(analyzer.lookup('skies'))

# expect the result `(('sky+N+Pl', 0.0),)`, i.e. output "a noun 'skies' in plural with a zero weight".
