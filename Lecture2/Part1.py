# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 2
#
# ## 1. Finite-State Basics
#
# Recall the finite-state transducer (FST) for purely concatenative I&A (Item and Arrangement)
# English noun inflection from Lecture 1:
#
# <img src="img/noun_inflection.png">
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
# <img src="img/three_word_language.png">
#
# * Inputs to the automaton are _symbols_ like: m, e, c.
# * The set of valid symbols that the automaton will accept is its _alphabet_: { a, c, e, g, i, m, n, o, r, s, t }.
# * The sequences of symbols that the automaton will accept are _words_ like: canto, mesa.
# * The entire set of words that the automaton accepts or recognizes is its _language_: { canto, mesa, tigre }.
#
# Sharing structure in minimal networks:
#
# <img src="img/fat_father.png">
#
# <img src="img/clear_clever_ear_ever.png">
#
# Removing a word from a minimal network may actually increase the size of the network!
#
# <img src="img/clear_clever_ever.png">
#
# ## 2. Set Theory for Finite-State Networks
#
# Examples of sets:
#
# <img src="img/two_sets.png">
#
# <img src="img/empty_set.png">
#
# Some sets viewed as networks:
#
# <img src="img/empty_network.png">
#
# <img src="img/empty_string_network.png">
#
# Some infinite sets:
#
# <img src="img/zero_or_more_a.png">
#
# <img src="img/universal_language.png">
#
# Relations:
#
# <img src="img/lowercase2uppercase.png">
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
# <img src="img/union_of_sets.png">
#
# For instance, the union of the sets `{"clear", "clever", "ear", "ever"}` and `{"fat", "father"}` is
# `{"clear", "clever", "ear", "ever", "fat", "father"}`.
#
# The union shown as a network:
#
# <img src="img/union_of_sets_as_network.png">
#
# Intersection of sets
#
# <img src="img/intersection_of_sets.png">
#
# For instance, the intersection of sets `{}` and `{}` is `{}`
#
# Subtraction of one set from another
#
# <img src="img/subtraction_of_sets.png">
#
# For instance, the subtraction of sets `{}` and `{}` is `{}`
#
# Concatenation of sets
#
# <img src="img/concatenation_of_sets.png">
#
# Composition of transducers
#
# <img src="img/">
#
# <img src="img/">
#
# Another composition of transducers
#
# <img src="img/">
#
# Projection
#
# * Projection is extracting one side of a relation.
# * The upper projection of `<"cat", "CHAT">` is "cat".
# * The lower projection of `<"cat", "CHAT">` is "CHAT".
#
# <img src="img/">
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
# Recall the finite-state transducer for purely concatenative I&A English
# noun inflection (from previous lecture):
#
# <img src="img/noun_inflection.dot">
#
# A more compact finite-state transducer for I&P English noun inflection:
#
# <img src="img/noun_inflection_compact.dot">
#
# ### Cascade of transducers: Rule 1
#
# Insert 'e' after the end of the stem in front of 's', if the stem ends in
# 's', 'x', 'ch', 'sh' or 'y'.
#
# Expressed as an xfst rule:
#
# `define InsertE   [. .] -> e || [ s | x | c h | s h | y ] %^ _ s ;`
#
# <img src="img/InsertE.png">
#
# ### Cascade of transducers: Rule 2
#
# Rewrite 'y' as 'i' when followed by the end of the stem, which is
# further followed by 'e'.
#
# Expressed as an xfst rule:
#
# `define YToI    y -> i || _ %^ e ;`
#
# <img src="img/YToI.png">
#
# ### Cascade of transducers: Rule 3
#
# Remove the end of stem marker
#
# Expressed as an xfst rule:
#
# `define CleanUp    %^ -> 0 ;`
#
# <img src="img/CleanUp.png">
#
# ### Cascade equivalent to single FST
#
# <img src="img/cascade1.png">
#
# When our lexicon is composed with our rules, we can actually produce one
# single FST and 'jump' from the lexical-form input straight to the final
# output in one go, without producing the intermediate steps.
#
# ### The order of the rules matters!
#
# What would happen if we reordered the rules (below) used in our simple
# English noun morphology?
#
# <img src="img/cascade2.png">
#
# ### xfst notation explained in context
#
# ## 4. Example: English adjectives
#
# ### Lexicon (lexc) of some English adjectives
#
# ```
# ...
# ```
#
# ### Suggested xfst script for English adjectives
#
# ```
# ...
# ```
#
# ### Corrected xfst script for English adjectives
#
# ```
# ...
# ```
#
# More information
#
# * Chapter 1 of the Beesley & Karttunen book: "A Gentle Introduction"
# * Chapter 3 of the Beesley & Karttunen book: "The xfst Interface"
#

