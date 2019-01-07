# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 5
#
# ## Section 1: Big picture
#
# ### Lecture 1: lexc
#
# "Lexicon without any replace rules"
#
# <img src="img/big_picture_lexc.png">
#
# ### Lectures 2 and 3: xfst and twolc
#
# "Lexicon combined with replace rules"
#
# <img src="img/big_picture_xfst_and_twolc.png">
#
# ### Lecture 4?: xfst / regular expressions 
#
# "Rules without much of a lexicon" 
#
# <img src="img/big_picture_xfst_and_regexps.png">
#
# ## Section 2: Guessers and stemmers
#
# ### Increased coverage with guessers 
#
# * Section 9.5.4 in the Beesley & Karttunen book
# * A finite-state morphological analyzer only recognizes the words that are included in its lexc lexicon.
# * It may take several person-months (or even years) of work to build up a lexicon with the tens of thousands of stems necessary for broad coverage of real text.
# * As an alternative, or a complement, one can use
#   * guessers
#   * stemmers
#   * unsupervised morphology
#
# ### Definition of a guesser
#
# * A guesser is designed to analyze words that are based on any phonologically possible stem.
# * The set of phonologically possible stems is definable, more or less precisely, using regular expressions and scripts.
# * Useful
#   * as a general backup when normal morphological analysis fails
#   * for suggesting new stems that need to be added to the lexicon
#
# ### Case study: Esperanto verb guesser lexicon
#
# <img src="img/esperanto_lexc.png">
#
# ### Case study: Esperanto verb guesser xfst script
#
"""
clear stack

! We limit ourselves here to lower case letters and ignore some Esperanto letters not found in the
! ASCII character set
define Vowel     a | e | i | o | u ;
define ConsClust b | c | d | f | g | h | j | k | l | m | n | p | r | s | t | v | z |
                 k r | p r | t r | g r | b r | d r | s k | s p | s t ;

                 ! Each verb root must be of the format Cc V Cc V Cc V Cc ..., where the first consonant cluster Cc is
                 ! optional and it must be followed by at least one pair of V Cc ( = vowel + consonant cluster):
                 define PossibleVerbRoot  ( ConsClust ) [ [ Vowel ] [ ConsClust ] ]+ "+Guess":0 ;

                 ! The lexc description is compiled and pushed on the stack
                 read lexc esperanto.lexc

                 ! Using the 'substitute defined' command, the placeholder symbol is replaced by the value of PossVerbRoot
                 substitute defined PossibleVerbRoot for ^GUESSVERBROOT

                 ! Make verb vocabulary ready to use
                 define AllPossibleVerbs ;
                 regex AllPossibleVerbs ;
"""
# ### Case study: Esperanto verb guesser example output
#
#
# Try: up donadas, random-upper, random-lower
#
# don+Guess+Verb+Cont+Pres
# don+Verb+Cont+Pres
# donad+Guess+Verb+Pres
#
# dip+Guess+Verb+Fut
# egrust+Guess+Verb+Subj
# fust+Guess+Verb+Fut
# obr+Guess+Verb+Cont+Fut
# opop+Guess+Verb+Cond
#
# etros
# hemodas
# jumadis
# soski
# tozezus
# ugrucas
# vabis
