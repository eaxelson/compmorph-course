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
# Examples of sets:
#
# <img src="two_sets.png">
#
# <img src="empty_set.png">
#
# Some sets viewed as networks:
#
# <img src="empty_network.png">
#
# <img src="empty_string_network.png">
#
# Some infinite sets:
#
# <img src="zero_or_more_a.png">
#
# <img src="universal_language.png">
#
# Relations:
#
# <img src="lowercase2uppercase.png">
#
# The example above shows an infinite relation containing pairs, such as
# `{<"dog","DOG">,<"cat","CAT">,<"mouse","MOUSE">,...}`
#
# We can also have relations between lexical forms and surface forms, such as:
# ```
# {<"cantar+Verb+PresInd+1P+Sg", "canto">,
#  <"cantar+Verb+PresInd+1P+Pl","cantamos">,
#  <"canto+Noun+Masc+Sg","canto">, ...}
#
# ```
#
# Union of sets
#
# <img src="union_of_sets.png">
#
# For instance, the union of the sets `{"clear", "clever", "ear", "ever"}` and `{"fat", "father"}` is
# `{"clear", "clever", "ear", "ever", "fat", "father"}`.
#
# The union shown as a network:
#
# <img src="union_of_sets_as_network.png">
#
# Intersection of sets
#
# <img src="intersection_of_sets.png">
#
# For instance, the intersection of sets `{}` and `{}` is `{}`
#
# Subtraction of one set from another
#
# <img src="subtraction_of_sets.png">
#
# For instance, the subtraction of sets `{}` and `{}` is `{}`
#
# Concatenation of sets
#
# <img src="concatenation_of_sets.png">
#
# Composition of transducers
#
# <img src="">
#
# <img src="">
#
# Another composition of transducers
#
# <img src="">
#
# Projection
#
# * Projection is extracting one side of a relation.
# * The upper projection of `<"cat", "CHAT">` is "cat".
# * The lower projection of `<"cat", "CHAT">` is "CHAT".
#
# <img src="">
#
# ### Set operations expressed in the xfst language
#
# ```
# [ A | B ] denotes the union of the two languages or relations A and B ("or"-operation).
# [ A & B ] denotes the intersection ("and"-operation).
# [ A - B ] denotes the subtraction of B from A.
# [ A B ] denotes the concatenation.
# [ A .o. B ] denotes the composition of the relations.
# A.u denotes the upper (i.e. input) projection.
# A.l denotes the lower (o.e. output) projection.
# ```
#
# ## 3. Item & Process morphology using xfst rules
#
# 
