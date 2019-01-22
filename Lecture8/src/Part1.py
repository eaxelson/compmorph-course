# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 8
#
# * (1.) Optimizing unweighted finite-state networks
# * (2.) Optimizing weighted finite-state networks
#
# ## 1. Optimizing unweighted finite-state networks
#
# Let’s first create a noun lexicon and add word stems to it.
#
# <img src="img/noun_lexicon.png">

from hfst_dev import HfstIterableTransducer, EPSILON
noun_lexicon = HfstIterableTransducer()
add = noun_lexicon.add_transition

# set start and end state numbers
start_state = 1
end_state = 8

# Add 'kisko'
state = 2
add(start_state, state, EPSILON, EPSILON, 0.0)
for symbol in list('kisko'):
    add(state, state+1, symbol, symbol, 0.0)
    state += 1
# equivalent to:
# add(2, 3, 'k', 'k', 0.0)
# add(3, 4, 'i', 'i', 0.0)
# add(4, 5, 's', 's', 0.0)
# add(5, 6, 'k', 'k', 0.0)
# add(6, 7, 'o', 'o', 0.0)

add(state, end_state, EPSILON, EPSILON, 0.0)

# skip end state
assert(state == 7)
state += 2

# Test the result:
print(noun_lexicon)

# Add rest of the lexemes
for lexeme in ('kissa','koira','kori','koulu','taulu','tori','tuoksu'):
    add(start_state, state, EPSILON, EPSILON, 0.0)
    for symbol in list(lexeme):
        add(state, state+1, symbol, symbol, 0.0)
        state += 1
    add(state, end_state, EPSILON, EPSILON, 0.0)
    state += 1

# Does it look right:
print(noun_lexicon)

test_lexicon = HfstIterableTransducer(noun_lexicon)
test_lexicon.add_transition(0, 1, EPSILON, EPSILON, 0.0)
test_lexicon.set_final_weight(8, 0.0)

from hfst_dev import HfstTransducer, regex
tr = HfstTransducer(test_lexicon)
tr.minimize()
result = regex('{kisko}|{kissa}|{koira}|{kori}|{koulu}|{taulu}|{tori}|{tuoksu}')
assert(result.compare(tr))

# Then let’s create a continuation lexicon with case endings and start populating it.
#
# <img src="img/continuation_lexicon.png">
#
# Then we tie the lexicons together and also add an epsilon transition from the end of the stem lexicon to its beginning in order to allow compound words
#
# <img src="img/compound_lexicon.png"> 
#
# Next let’s add a lexicon for verb stems.
#
# <img src="img/lexicon_verb_stems.png">
#
# ... and a continuation lexicon for present-tense person endings (mainly)
#
# <img src="img/lexicon_person_endings.png">
#
# Let’s tie the verb stem lexicon together with the endings lexicon.
#
# <img src="img/lexicon_verbs_and_endings.png">
#
# ... and let’s tie the whole network together with a start state and end state
#
# <img src="img/lexicon_tied_together.png">
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
# <img src="img/lexicon_epsilon_transitions.png">
#
# To start determinizing the network...
#
# * 1. We would merge the states 3, 10, 16, 22, 27, and 70 into one single, new state.
# * 2. We would create one transition with the symbol “k” from the initial state to our new state. (Not shown in the picture on the next page.)
#
# <img src="img/determinizing_the_network_1.png">
#
# * 3. Then, from the new state, the symbol “o” takes us to the states 17, 23 or 28, so we would merge these states into one new state, too.
#
# <img src="img/determinizing_the_network_2.png">
#
# * 4. And the symbol “i” takes us to the states 4, 11, and 71, so we keep merging states and updating the transitions.
#
# <img src="img/determinizing_the_network_3.png">



# Furthermore, there is another disadvantage with the original network
#
# * The network is unnecessarily large
#   * There are some “tails” that occur in many places that could be merged.
#   * For instance, the ends of the stems “kori” and “tori” are identical, as are the ends of the stems “koulu” and “taulu”.
#   * Determinization will not fix these issues, so we can use a separate minimization algorithm.
#
# <img src="img/minimizing_the_network_1.png">
#
# <img src="img/minimizing_the_network_2.png">
#
# Note: There have been some simplifications in our presentation
#
# * The epsilon transition back to the beginning that produces compound words is nasty:
#   * Full determinization may actually bloat the size of the network.
#   * Consider, for instance, if we had the stem “koulu” that can get an “a” appended for partitive (“koulua”), but in addition, “a” could be the beginning of a second stem, such as “aamiainen” (“kouluaamiainen”).
#   * Then, we would need one node in the network that is the starting point for all stems starting in “a” as the first stem in a word and another node with all the stems starting in “a” plus the endings starting in “a”.
#
# <img src="img/full_determinization.png">
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

# ## 2. Optimizing weighted finite-state networks
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
# ```
#
# Then we get the following probabilities for the full word forms “tuoksua”:
#
# * `Prob(tuoksua as a noun) = Prob(Noun) × Prob(tuoksu | Noun) × Prob(Noun ending -a for partitive case) = 0.5 × 0.0001 × 0.1 = 0.000005`
# * `Prob(tuoksua as a verb) = Prob(Verb) × Prob(tuoksu | Verb) × Prob(Verb ending -a for infinitive) = 0.3 × 0.001 × 0.05 = 0.000015`
# * `Prob(tuoksua as a noun or verb) = Prob(tuoksua as a noun) + Prob(tuoksua as a verb) =  0.000005 + 0.000015 = 0.00002`
#
# Shown as a network with probability weights:
#
# <img src="img/network_with_probability_weights.png">
#
# However, usually weights are not probabilities as such.
#
# ### 2.0. Semirings
#
# * Let’s replace the probabilities with some generic weights and replace the operators × and + with the generic semiring operators ⊗ and ⊕
#   * `Weight(tuoksua as a noun) = Weight(Noun) ⊗ Weight(tuoksu | Noun) ⊗ Weight(Noun ending -a for partitive case)`
#   * `Weight(tuoksua as a verb) = Weight(Verb) ⊗ Weight(tuoksu | Verb) ⊗ Weight(Verb ending -a for infinitive)`
#   * `Weight(tuoksua as a noun or verb) = Weight(tuoksua as a noun) ⊕ Weight(tuoksua as a verb)`
#
# ### 2.1. Probability semiring
#
# * The weights should be interpreted as probabilties
# * The operator ⊗ should be interpreted as multiplication ×
# * The operator ⊕ should be interpreted as addition +
# * This is exactly what we have seen in our example already
#
# ### 2.2. Log semiring
#
# * The weights should be interpreted as negative logprobs: for instance, – log Prob(tuoksu | Noun)
# * The operator ⊗ should be interpreted as addition +
# * The operator ⊕ should be interpreted as the rather complex operation: w1 ⊕ w2 = – log (10<sup>-w1</sup> + 10<sup>-w2</sup>)  (if we use 10 as our base; it can be something else, too)
# * Why? Because if w1 = – log<sub>10</sub> p1 and w2 = – log<sub>10</sub> p2 and p1 and p2 are probabilities, then w1 ⊕ w2 = – log<sub>10</sub>(10<sup>– log<sub>10</sub> p1</sup> + 10<sup>– log<sub>10</sub> p2</sup>) =  – log<sub>10</sub>(p1 + p2) (This is the logprob of the sum of two probabilities)
#
# Shown as a network with logprob weights in the log semiring
#
# <img src="img/network_with_logprob_weights.png">
#
# ### 2.3. Tropical semiring
#
# * The weights can still be interpreted as negative logprobs: for instance, –log(Prob(tuoksu | Noun))
# * The operator ⊗ should still be interpreted as addition +
# * The operator ⊕ is simplified and picks the minimum, that is, the path with lower overall weight: w1 ⊕ w2 = min(w1, w2) = { w1 if w1 < w2; w2 otherwise }
#
# Shown as a network with logprob weights in the tropical semiring:
#
# <img src="img/network_with_tropical_weights.png">
#
# Another example of weighted determinization in the tropical semiring:
#
# <img src="img/weighted_determinization_example.png">
#
# Weight pushing and minimization:
#
# <img src="img/weight_pushing_and_minimization.png">
#
# Mehryar Mohri did not work on morphology,but on automatic speech recognition:
#
# <img src="img/speech_recognition.png">
#
# ### 2.4. Further reading
#
# * To learn more, you can read the full article by Mohri et al. at: http://www.cs.nyu.edu/~mohri/pub/csl01.pdf
# * There are more similar articles, such as the version that was actually published in Computer Speech and Language in 2002.
# * Or look at the OpenFST library: http://www.cs.columbia.edu/~mohri/
