# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS
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
# * [HFST toolset](https://hfst.github.io)
#
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
#
#
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
# | Model/Tool | hfst-twolc | hfst-lexc | hfst-xfst
# | - | - | - | - |
# | Word & Paradigm |  | ✔ | ✔ |
# | Item & Arrangement |  | ✔ | ✔ |
# | Item & Process | ✔ |  | ✔ |
#
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
#   - when we want to *normalize* text, such that we only care about the base form (lemma) of every word in the text; this is used, for instance, in *information retrieval*.
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
#
# ## 6. A Finite-State Transducer that implements a morphological generator
#
# Below is a finite-state transducer (FST) for purely concatenative I&A English noun inflection.
# _Root_ is the initial state and _#_ the final one. The yellow circles represent _states_
# and arrows _transitions_ between the states. Above each transition, there is the input
# that the transition _consumes_ and the output that it _produces_, separated with a colon ":".
# The "ε:ε" signifies the _epsilon_ transition which is possible without consuming
# any input or producing any output. We will return to finite-state transducers in more detail
# in the next part.
#
# <img src="image11.png">
#
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
# ### 7.3 Define the Nouns lexicon
#
# ```
# 
# ```
#
# ### 7.4 Continuation lexicons for the N paradigm
#
# ```
# ...
# ```
#
# ### 7.5 Continuation lexicons for the N_s paradigm
#
# ```
# ...
# ```
#
# ### 7.6 Continuation lexicons for the N_y paradigm
#
# ```
# ...
# ```
#
# ### 7.7 Continuation lexicons for possessive ending
#
# ```
# ...
# ```
#
# ### 7.8 
#
# ```
# ...
# ```
#
# Note that END siginifies the end of lexc file.
#
#
