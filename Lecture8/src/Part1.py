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

## 2. Optimizing unweighted finite-state networks
#
# Optimizing weighted finite-state networks is basically the same as unweighted networks, but the weights may mess up things.
# We would like the optimized weighted network to produce the same weights as the unoptimized network.
#
# Assume the following probabilities:
#
# ```
# Prob(Noun) = 0.5
# Prob(Verb) = 0.3
# Prob(tuoksu | Noun) = 0.0001
# Prob(Noun ending -a for partitive case) = 0.1
# Prob(tuoksu | Verb) = 0.001
# Prob(Verb ending -a for infinitive) = 0.05
# ´´´
#
# Then we get the following probabilities for the full word forms “tuoksua”:
#
# * `Prob(tuoksua as a noun) = Prob(Noun) × Prob(tuoksu | Noun) × Prob(Noun ending -a for partitive case) = 0.5 × 0.0001 × 0.1 = 0.000005`
# * `Prob(tuoksua as a verb) = Prob(Verb) × Prob(tuoksu | Verb) × Prob(Verb ending -a for infinitive) = 0.3 × 0.001 × 0.05 = 0.000015`
# * `Prob(tuoksua as a noun or verb) = Prob(tuoksua as a noun) + Prob(tuoksua as a verb) =  0.000005 + 0.000015 = 0.00002`
#
# Shown as a network with probability weights:
#
# However, usually weights are not probabilities as such.
#
# ### Semirings
#
# * Let’s replace the probabilities with some generic weights and replace the operators × and + with the generic semiring operators ⊗ and ⊕
#   * `Weight(tuoksua as a noun) = Weight(Noun) ⊗ Weight(tuoksu | Noun) ⊗ Weight(Noun ending -a for partitive case)`
#   * `Weight(tuoksua as a verb) = Weight(Verb) ⊗ Weight(tuoksu | Verb) ⊗ Weight(Verb ending -a for infinitive)`
#   * `Weight(tuoksua as a noun or verb) = Weight(tuoksua as a noun) ⊕ Weight(tuoksua as a verb)`
#
# ### 1. Probability semiring
#
# * The weights should be interpreted as probabilties
# * The operator ⊗ should be interpreted as multiplication ×
# * The operator ⊕ should be interpreted as addition +
# * This is exactly what we have seen in our example already
#
# ### 2. Log semiring
#
# * The weights should be interpreted as negative logprobs: for instance, – log Prob(tuoksu | Noun)
# * The operator ⊗ should be interpreted as addition +
# * The operator ⊕ should be interpreted as the rather complex operation: w1 ⊕ w2 = – log (10-w1 + 10-w2)  (if we use 10 as our base; it can be something else, too)
# * Why? Because if w1 = – log10 p1 and w2 = – log10 p2 and p1 and p2 are probabilities, then w1 ⊕ w2 = – log10 (10– log10 p1 + 10– log10 p2) =  – log10 (p1 + p2) (This is the logprob of the sum of two probabilities)
#
# Shown as a network with logprob weights in the log semiring
#
# ### 3. Tropical semiring
#
# * The weights can still be interpreted as negative logprobs: for instance, – log Prob(tuoksu | Noun)
# * The operator ⊗ should still be interpreted as addition +
# * The operator ⊕ is simplified and picks the minimum, that is, the path with lower overall weight: w1 ⊕ w2 = min(w1, w2) = { w1 if w1 < w2; w2 otherwise }
#
# Shown as a network with logprob weights in the tropical semiring:
#
# Another example of weighted determinization in the tropical semiring:
#
# Weight pushing and minimization:
#
# Mehryar Mohri did not work on morphology,but on automatic speech recognition:
#
# ### Further reading
# * To learn more, you can read the full article by Mohri et al. at: http://www.cs.nyu.edu/~mohri/pub/csl01.pdf
# * There are more similar articles, such as the version that was actually published in Computer Speech and Language in 2002.
# * Or look at the OpenFST library: http://www.cs.columbia.edu/~mohri/
