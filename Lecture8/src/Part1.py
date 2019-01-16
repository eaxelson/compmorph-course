# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 8
#
# ## 1. Optimizing unweighted finite-state networks
#
# Let’s first create a noun lexiconand add word stems to it.
#
# Then let’s create a continuation lexicon with case endings and start populating it.
#
# Then we tie the lexicons togetherand also add an epsilon transition from the end of the stem lexiconto its beginning in order to allow compound words
#
# Next let’s add a lexicon for verb stems.
#
# ... and a continuation lexicon for present-tense person endings (mainly)
#
# Let’s tie the verb stem lexicon together with the endings lexicon.
#
# ... and let’s tie the whole network together with a start state and end state
#
# The network is now ready. It has some advantages
#
# * The structure is logical
# * Building the network by adding words and endings to it (through the union operation) is simple and fast
#
# However, there are also some disadvantages
#
# * The automaton is non-deterministic and contains epsilon transitions
#   * This means that from a specific state, some symbol s can take you to more than one another state.
#   * For instance, from the initial state 103, the symbol “k” could take you to state 3, 10, 16, 22, 27, or 70.
#   * Imagine a scenario with a more realistic, larger vocabulary: using the network would be very slow, because of all the paths that have to be investigated.
#
# To start determinizing the network...
#
# * 1. We would merge the states 3, 10, 16, 22, 27, and 70 into one single, new state.
# * 2. We would create one transition with the symbol “k” from the initial state to our new state. (Not shown in the picture on the next page.)
#
# * 3. Then, from the new state, the symbol “o” takes us to the states 17, 23 or 28, so we would merge these states into one new state, too.
#
# * 4. And the symbol “i” takes us to the states 4, 11, and 71, so we keep merging states and updating the transitions.
#
# Furthermore, there is another disadvantage with the original network
#
# * The network is unnecessarily large
#   * There are some “tails” that occur in many places that could be merged.
#   * For instance, the ends of the stems “kori” and “tori” are identical, as are the ends of the stems “koulu” and “taulu”.
#   * Determinization will not fix these issues, so we can use a separate minimization algorithm.
#
# Note: There have been some simplifications in our presentation
#
# * The epsilon transition back to the beginning that produces compound words is nasty:
#   * Full determinization may actually bloat the size of the network.
#   * Consider, for instance, if we had the stem “koulu” that can get an “a” appended for partitive (“koulua”), but in addition, “a” could be the beginning of a second stem, such as “aamiainen” (“kouluaamiainen”).
#   * Then, we would need one node in the network that is the starting point for all stems starting in “a” as the first stem in a word and another node with all the stems starting in “a” plus the endings starting in “a”.
#
# * One might actually choose not to do a full determinization, but keep the epsilon transitions, for instance.
#
# Acceptors vs. transducers?
#
# * In the examples above, we have shown acceptors, with only an input symbol on the arcs
#   * Such as: a b c d
# * If we had a transducer, we would have pairs of symbols (input:output)
#   * Such as: a:a a:b b:b c:e
# * Determinization and minimization work the same in both cases.
#   * We just need to interpret the pairs of symbols as one single symbol, so a:a is another symbol than a:b.
#
# Algorithms
#
# * Determinization
#   * For instance: https://www.tutorialspoint.com/automata_theory/ndfa_to_dfa_conversion.htm
# * Minimization
#   * For instance: http://www.cs.engr.uky.edu/~lewis/essays/compilers/min-fa.html (todo: check)
#
# 



#
#
#
# <img src="img/inflection_of_kitaab.png">
