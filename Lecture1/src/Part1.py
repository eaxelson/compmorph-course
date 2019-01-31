# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 1
#
# <ul>
# <li>1. <a href="#1.-Prerequisites">Prerequisites</a></li>
# <li>2. <a href="#2.-Course-material">Course material</a></li>
# <li>3. <a href="#3.-Course-overview">Course overview</a></li>
# <li>4. <a href="#4.-Hockett's-models-of-morphology">Hockett's models of morphology</a></li>
# <li>5. <a href="#5.-Morphological-generators-and-analyzers">Morphological generators and analyzers</a></li>
# <li>6. <a href="#6.-A-Finite-State-Transducer-that-implements-a-morphological-generator">A Finite-State Transducer that implements a morphological generator</a></li>
# <li>7. <a href="#7.-Lexc-code-that-represents-this-transducer">Lexc code that represents this transducer</a></li>
# </ul>
#
# ## HFST - Helsinki Finite-State Technology
#
# The HFST toolkit is intended for processing natural language
# morphologies. The toolkit is demonstrated by wide-coverage
# implementations of a number of languages of varying morphological
# complexity. HFST is written mainly in C++, but there is also a Python interface
# which is demonstrated on these notebooks.
#
# ## 1. Prerequisites
#
# <ul>
# <li>Foundations of general linguistics</li>
# <li>Basic knowledge on how to use a computer</li>
# <li>Some programming experience is desirable</li>
# <li>Knowledge of Natural Language Processing (NLP) is also a plus</li>
# </ul>
#
# ## 2. Course material
#
# If you want a book:
#
# <ul>
# <li>Kenneth R. Beesley and Lauri Karttunen: <a href="http://press.uchicago.edu/ucp/books/book/distributed/F/bo3613750.html">Finite State Morphology</a>, CSLI Publications, 2003</li>
# <li>Daniel Jurafsky and James H. Martin, Speech and Language Processing, Prentice Hall, second edition, 2009</li>
# </ul>
#
# Links:
#
# <ul>
# <li>HFST <a href="https://hfst.github.io">main page</a>.</li>
# <li>For installation of the HFST package for Python, see our <a href="https://pypi.org/project/hfst_dev/">PyPI pages</a>.</li>
# <li>For more information about the interface, see our <a href="https://github.com/hfst/python-hfst-4.0/wiki">Github wiki pages</a>.</li>
# </ul>
#
# First, import the package and list its contents with `help`.

import hfst_dev
help(hfst_dev)

# Then, see for more information on some of the functions, e.g. `compile_lexc_file`.

help(hfst_dev.compile_lexc_file)

# Also print the version number of the package.

print(hfst_dev.__version__)

# ## 3. Course overview
#
# <table>
# <tr> <th>Lecture</th> <th>Topics</th> </tr>
# <tr> <td>1</td> <td>Theories of morphology, generators and analyzers, lexc</td> </tr>
# <tr> <td>2</td> <td>Finite-state basics, xfst rules</td> </tr>
# <tr> <td>3</td> <td>Disambiguation, probabilities, finite-state networks summarized</td> </tr>
# <tr> <td>(4)</td> <td>(Machine learning)</td> </tr>
# <tr> <td>5</td> <td>Guessers, stemmers, regular expressions in xfst</td> </tr>
# <tr> <td>6</td> <td>Twolc, two-level rules</td> </tr>
# <tr> <td>7</td> <td>Flag diacritics, non-concatenative morphology</td> </tr>
# <tr> <td>8</td> <td>Optimization of finite-state networks</td> </tr>
# </table>

# ## 4. Hockett's models of morphology
#
# ### 4.1. Word and Paradigm (W&P), Example: Finnish nouns
#
# <table>
# <tr> <th>Numbers/Cases</th> <th>Singular</th> <th>Plural</th> </tr>
# <tr> <th>Nominative</th> <td>susi</td> <td>sudet</td> </tr>
# <tr> <th>Genitive</th> <td>suden</td> <td>susien, sutten</td> </tr>
# <tr> <th>Partitive</th> <td>sutta</td> <td>susia</td> </tr>
# <tr> <th>Inessive</th> <td>sudessa</td> <td>susissa</td> </tr>
# <tr> <th>Elative</th> <td>sudesta</td> <td>susista</td> </tr>
# <tr> <th>Illative</th> <td>suteen</td> <td>susiin</td> </tr>
# <tr> <th>Adessive</th> <td>sudella</td> <td>susilla</td> </tr>
# <tr> <th>Ablative</th> <td>sudelta</td> <td>susilta</td> </tr>
# <tr> <th>Allative</th> <td>sudelle</td> <td>susille</td> </tr>
# <tr> <th>Essive</th> <td>sutena</td> <td>susina</td> </tr>
# <tr> <th>Translative</th> <td>sudeksi</td> <td>susiksi</td> </tr>
# <tr> <th>Instructive</th> <td>-</td> <td>susin</td> </tr>
# <tr> <th>Abessive</th> <td>sudetta</td> <td>susitta</td> </tr>
# <tr> <th>Comitative</th> <td>-</td> <td>susine(en)</td> </tr>
# </table>

# ### 4.2. Item and Arrangement (I&A)
#
# #### Morphemes and allomorphs
#
# <ul>
#  <li>"SUSI": susi, sude-, sute-, sut-, sus-</li>
#  <li>Number:</li>
#   <ul>
#    <li>Singular: ∅ (or no morpheme at all: unmarked)</li>
#    <li>Plural: -t, -i-, -j-</li>
#   </ul>
#  <li>Case:</li>
#   <ul>
#     <li>Genitive: -n, -en, -den, -tten</li>
#     <li>Partitive: -a, -ä, -ta, -tä</li>
#     <li>Etc.</li>
#   </ul>
# </ul>
#
# #### The allomorphs occur in a specific distribution
#
# <ul>
#  <li>E.g., sus- in all plural forms except nominative.</li>
#  <li>No allomorph is more "basic" than any other.</li>
# </ul>
#
# ### 4.3. Item and Process (I&P)
#
# We have roots or bases of morphemes and different processes apply to them.
#
# <ul>
#  <li>Nominative: word final 'e' becomes 'i'; 't' in front of 'i' becomes 's' 🡒 "susi"</li>
#  <li>Genitive: add suffix '+n'; soften 't' to 'd' in closed syllable 🡒 "suden"</li>
#  <li>Etc.</li>
# </ul>
#
# ### 4.4. Corresponding HFST tools
#
# <table>
# <tr> <th>Model/Tool</th> <th><a href="https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_twolc_file-inputfilename-outputfilename-kwargs">twolc</a></th> <th><a href="https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_lexc_file-filename-kwargs">lexc</a></th> <th><a href="https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_xfst_file-filename-kwargs">xfst</a></th> </tr>
# <tr> <th>Word & Paradigm</th> <td> </td> <td>✔</td> <td>✔</td> </tr>
# <tr> <th>Item & Arrangement</th> <td> </td> <td>✔</td> <td>✔</td> </tr>
# <tr> <th>Item & Process</th> <td>✔</td> <td> </td> <td>✔</td> </tr>
# </table>
#
# Check how they work with `help` command.
#
# #### twolc:

help(hfst_dev.compile_twolc_file)

# #### lexc:

help(hfst_dev.compile_lexc_file)

# #### xfst:

help(hfst_dev.compile_xfst_file)

# #### interactive version of xfst:

help(hfst_dev.start_xfst)

# ## 5. Morphological generators and analyzers
#
# ### 5.1. Morphological generator
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
# ### 5.2. Morphological analyzer
#
# * Input (surface form): `cat's`
# * Output (lexical form): `cat+N+Sg+Poss`
# * An analyzer produces the opposite mapping compared to the generator:
#   - The input of the generator is the output of the analyzer.
#   - The output of the analyzer is the input of the generator.
# * An analyzer is very useful, for instance:
#   - when we want to parse natural language text syntactically
#   - when we want to <i>normalize</i> text, such that we only care about the base form (lemma) of every word in the text; this is used, for instance, in <i>information retrieval</i>.
#
# ### 5.3. Some simple noun paradigms in English
#
# #### Paradigm: N
#
# <table>
# <tr> <td><b>cat</b></td> <td>+Sg (singular)</td> </tr>
# <tr> <td><b>cat|s</b></td> <td>+Pl (plural)</td> </tr>
# <tr> <td><b>cat|'s</b></td> <td>+Sg +Poss (singular possessive)</td> </tr>
# <tr> <td><b>cat|s'</b></td> <td>+Pl +Poss (plural possessive)</td> </tr>
# </table>
#
# <i>Similarly:</i> dog, pet, book, hill, fan
#
# #### Paradigm: N_s
#
# <table>
# <tr> <td><b>kiss</b></td> <td>+Sg (singular)</td> </tr>
# <tr> <td><b>kiss|es</b></td> <td>+Pl (plural)</td> </tr>
# <tr> <td><b>kiss|'s</b></td> <td>+Sg +Poss (singular possessive)</td> </tr>
# <tr> <td><b>kiss|es|'</b></td> <td>+Pl +Poss (plural possessive)</td> </tr>
# </table>
#
# <i>Similarly:</i> wish, mess, church, search, waitress
#
# Let's create a morphological generator and analyzer for this data.

# ## 6. A Finite-State Transducer that implements a morphological generator
#
# Below is a finite-state transducer (FST) for purely concatenative I&A English noun inflection
# for our simple example data.
# The yellow circles represent _states_ and the arrows represent _transitions_ between the states.
# State named <i>Root</i> is the initial state and state named <i>\#</i> the final one.
# Above each transition, there is the input
# that the transition <i>consumes</i> and the output that it <i>produces</i>, separated with a colon ":".
# The symbol ε is the <i>epsilon</i>, i.e. the empty symbol. On input side it means that no symbol is consumed
# and on output side that no symbol is produced.
# The "ε:ε" signifies the <i>epsilon transition</i> which is possible without consuming
# any input or producing any output.
# We will return to finite-state transducers in more detail in the next part.
#
# <img src="img/noun_inflection.png">

# ## 7. Lexc code that represents this transducer
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
# Note that `END` signifies the end of lexc file. It must be included at the end of each lexc file.
#
# ### 7.7. Compiling the lexc script into a transducer
#
# Finally, let's compile the lexc script into a transducer:

from hfst_dev import compile_lexc_script

generator = compile_lexc_script(
"""
Multichar_Symbols
        +N      ! Noun tag
        +Sg     ! Singular
        +Pl     ! Plural
        +Poss   ! Possessive form

LEXICON Root
        Nouns ; ! No input, no output

!
! NOUNS start here
!

LEXICON Nouns

cat     N ;
dog     N ;

church    N_s ;
kiss      N_s ;

beauty:beaut    N_y ;
sky:sk          N_y ;


! The noun lexica N and Num are used for stems without any alternation

LEXICON N
+N:0    Num ;

LEXICON Num
+Sg:0   PossWithS ;
+Pl:s   PossWithoutS ;

! The noun lexica N_s and Num_s are used for stems that end in a sibilant
! and need an extra inserted "e"

LEXICON N_s
+N:0    Num_s ;

LEXICON Num_s
+Sg:0   PossWithS ;
+Pl:es  PossWithoutS ;

! The noun lexica N_y and Num_y are used for stems with "y" -> "ie" alternation

LEXICON N_y
+N:0    Num_y ;

LEXICON Num_y
+Sg:y   PossWithS ;
+Pl:ies PossWithoutS ;

! Possessive endings: usually the singular is 's and the plural is '

LEXICON PossWithS
+Poss:'s     # ;
             # ; ! No ending: no input, no output

LEXICON PossWithoutS
+Poss:'      # ;
             # ; ! No ending: no input, no output

END
""", verbosity=2
)

# We could also write the script to a file and then call `compile_lexc_file`. Note that we set the keyword argument `verbosity` to `2`.
# Then we will get more information about the compilation process.
# You can test the above command also with `verbosity=1` and `verbosity=0` (or just leaving the argument out).
#
# Test the transducer:

print(generator.lookup('sky+N+Pl'))

# and expect the result `(('skies', 0.0),)`, i.e. <i>skies</i> with a zero _weight_. We will return to weights in later lectures.
#
# Next, _invert_ the transducer to get an analyzer:

from hfst_dev import HfstTransducer
analyzer = HfstTransducer(generator) # create a copy
analyzer.invert()
analyzer.minimize()

print(analyzer.lookup('skies'))

# and expect the result `(('sky+N+Pl', 0.0),)`, i.e. "the noun <i>sky</i> in plural with a zero weight".
#
# Let's check that inverting the analyzer produces a transducer equivalent to the generator:

analyzer.invert()
analyzer.minimize()
print(analyzer.compare(generator))
