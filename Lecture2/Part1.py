# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 2
#
# ## 1. Finite-State Basics
#
# Recall the finite-state transducer (FST) for purely concatenative I&A (Item and Arrangement)
# English noun inflection from Lecture 1:
#
# <img src="noun_inflection.png">
#
# The yellow circles represent _states_ or _nodes_ and the arrows represent _transitions_
# or _arcs_ between states. Each transition consumes an input symbol and produces an output symbol.
# The special symbol ε (the epsilon) on the input side means that no symbol is consumed
# and on the output side that no symbol is produced when following a given transition.
#
# A finite-state network that has only input symbols in the transitions is called
# a finite-state automaton (FSA). It does not produce output, but just recognizes
# (or rejects) input. Finite-state automaton for a 3-word language:
#
# <img src="three_word_language.png">
#
# * Inputs to the automaton are _symbols_ like: m, e, c.
# * The set of valid symbols that the automaton will accept is its _alphabet_: { a, c, e, g, i, m, n, o, r, s, t }.
# * The sequences of symbols that the automaton will accept are _words_ like: canto, mesa.
# * The entire set of words that the automaton accepts or recognizes is its _language_: { canto, mesa, tigre }.
#
# Sharing structure in minimal networks:
#
# <img src="fat_father.png">
#
# <img src="clear_clever_ear_ever.png">
#
# Removing a word from a minimal network may actually increase the size of the network!
#
# <img src="clear_clever_ever.png">
#
# ## 2. Set Theory for Finite-State Networks
#
# Examples of sets
#
# <img src="two_sets.png">
#
# <img src="empty_set.png">
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

