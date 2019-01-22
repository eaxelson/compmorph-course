# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 8
#
# * (1.) Optimizing unweighted finite-state networks
# * (2.) Optimizing weighted finite-state networks
#
# ## 1. Optimizing unweighted finite-state networks
#
# ### 1.1. Example lexicon
#
# Let’s first create a noun lexicon and add word stems to it.
#
# <img src="img/noun_lexicon.png">

from hfst_dev import HfstIterableTransducer, EPSILON
# This will be the entire lexicon
lexicon = HfstIterableTransducer()
add = lexicon.add_transition # shorter notation for adding transition
# define sublexicon start and end states
start_state = 1
end_state = 8
# and use consecutive numbering for states that will be added
# (remember to skip end state)
state = 2

# we could add lexemes manually, e.g.
#   add(2, 3, 'k', 'k', 0.0)
#   add(3, 4, 'i', 'i', 0.0)
#   add(4, 5, 's', 's', 0.0)
#   add(5, 6, 'k', 'k', 0.0)
#   add(6, 7, 'o', 'o', 0.0)
# but it is easier this way:
add(start_state, state, EPSILON, EPSILON, 0.0) # from start state to beginning of lexeme
for symbol in list('kisko'):
    add(state, state+1, symbol, symbol, 0.0)
    state += 1
add(state, end_state, EPSILON, EPSILON, 0.0) # from end of lexeme to end state

# skip end state
assert(state == 7)
state += 2

# Add rest of the lexemes
for lexeme in ('kissa','koira','kori','koulu','taulu','tori','tuoksu'):
    add(start_state, state, EPSILON, EPSILON, 0.0)
    for symbol in list(lexeme):
        add(state, state+1, symbol, symbol, 0.0)
        state += 1
    add(state, end_state, EPSILON, EPSILON, 0.0)
    state += 1

# test that the result is as intended
test_lexicon = HfstIterableTransducer(lexicon)
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

assert(state == 50)
state += 1
start_state = 50
end_state = 53

# Add case endings
for ending in ('a','lla','lle','lta','n'):
    # skip end state
    if state == end_state:
        state += 1
    add(start_state, state, EPSILON, EPSILON, 0.0)
    for symbol in list(ending):
        add(state, state+1, symbol, symbol, 0.0)
        state += 1
    add(state, end_state, EPSILON, EPSILON, 0.0)
    state += 1
# make case ending optional
add(50, 53, EPSILON, EPSILON, 0.0)

assert(state == 68)

# Then we tie the lexicons together and also add an epsilon transition from the end of the stem lexicon to its beginning in order to allow compound words
#
# <img src="img/compound_lexicon.png"> 

add(8, 50, EPSILON, EPSILON, 0.0)
add(8, 1, EPSILON, EPSILON, 0.0)

# test that the result is as intended
test_lexicon = HfstIterableTransducer(lexicon)
test_lexicon.add_transition(0, 1, EPSILON, EPSILON, 0.0)
test_lexicon.set_final_weight(53, 0.0)

tr = HfstTransducer(test_lexicon)
tr.minimize()
result = regex('[{kisko}|{kissa}|{koira}|{kori}|{koulu}|{taulu}|{tori}|{tuoksu}]+ ({a}|{lla}|{lle}|{lta}|{n})')
assert(result.compare(tr))

# Next let’s add a lexicon for verb stems.
#
# <img src="img/lexicon_verb_stems.png">

assert(state == 68)
start_state = 68
end_state = 75
state += 1

# Add verb stem endings
for stem in ('kisko','tuoksu'):
    # skip end state
    if state == end_state:
        state += 1
    add(start_state, state, EPSILON, EPSILON, 0.0)
    for symbol in list(stem):
        add(state, state+1, symbol, symbol, 0.0)
        state += 1
    add(state, end_state, EPSILON, EPSILON, 0.0)
    state += 1

# ... and a continuation lexicon for present-tense person endings (mainly)
#
# <img src="img/lexicon_person_endings.png">

assert(state == 83)
start_state = 83
end_state = 86
state +=1

# Add person endings
for ending in ('a','mme','n','t','tte','vat'):
    # skip end state
    if state == end_state:
        state += 1
    add(start_state, state, EPSILON, EPSILON, 0.0)
    for symbol in list(ending):
        add(state, state+1, symbol, symbol, 0.0)
        state += 1
    add(state, end_state, EPSILON, EPSILON, 0.0)
    state += 1

# make person ending optional
add(83, 86, EPSILON, EPSILON, 0.0)

assert(state == 103)

# Let’s tie the verb stem lexicon together with the endings lexicon.
#
# <img src="img/lexicon_verbs_and_endings.png">

add(75, 83, EPSILON, EPSILON, 0.0)

# ... and let’s tie the whole network together with a start state and end state
#
# <img src="img/lexicon_tied_together.png">

add(0, 1, EPSILON, EPSILON, 0.0)
add(0, 68, EPSILON, EPSILON, 0.0)
add(53, 103, EPSILON, EPSILON, 0.0)
add(86, 103, EPSILON, EPSILON, 0.0)
lexicon.set_final_weight(103, 0.0)

# test that the result is as intended
tr = HfstTransducer(lexicon)
tr.minimize()
result = regex("""
[ [{kisko}|{kissa}|{koira}|{kori}|{koulu}|{taulu}|{tori}|{tuoksu}]+ ({a}|{lla}|{lle}|{lta}|{n}) ]
| 
[ [{kisko}|{tuoksu}] ({a}|{mme}|{n}|{t}|{tte}|{vat}) ]
""")
assert(result.compare(tr))

# ### 1.2. The resulting network
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
#   * For instance, from the initial state 0, the symbol “k” could take you to state 3, 10, 16, 22, 27, or 70.
#   * Imagine a scenario with a more realistic, larger vocabulary: using the network would be very slow, because of all the paths that have to be investigated.
#
# <img src="img/lexicon_epsilon_transitions.png">
#
# ### 1.3. Determinization of the network
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

tr = HfstTransducer(lexicon)
tr.determinize()

# ### 1.4. Minimization of the network
#
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

tr = HfstTransducer(lexicon)
tr.minimize()

# ### 1.5. Further issues
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
# #### Acceptors vs. transducers?
#
# * In the examples above, we have shown acceptors, with only an input symbol on the arcs
#   * Such as: `a b c d`
# * If we had a transducer, we would have pairs of symbols (`input:output`)
#   * Such as: `a:a a:b b:b c:e`
# * Determinization and minimization work the same in both cases.
#   * We just need to interpret the pairs of symbols as one single symbol, so `a:a` is another symbol than `a:b`.
#
# #### Algorithms
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
# ### 2.1. Semirings
#
# * Let’s replace the probabilities with some generic weights and replace the operators × and + with the generic semiring operators ⊗ and ⊕
#   * `Weight(tuoksua as a noun) = Weight(Noun) ⊗ Weight(tuoksu | Noun) ⊗ Weight(Noun ending -a for partitive case)`
#   * `Weight(tuoksua as a verb) = Weight(Verb) ⊗ Weight(tuoksu | Verb) ⊗ Weight(Verb ending -a for infinitive)`
#   * `Weight(tuoksua as a noun or verb) = Weight(tuoksua as a noun) ⊕ Weight(tuoksua as a verb)`
#
# ### 2.2. Probability semiring
#
# * The weights should be interpreted as probabilties
# * The operator ⊗ should be interpreted as multiplication ×
# * The operator ⊕ should be interpreted as addition +
# * This is exactly what we have seen in our example already
#
# ### 2.3. Log semiring
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
# ### 2.4. Tropical semiring
#
# * The weights can still be interpreted as negative logprobs: for instance, –log(Prob(tuoksu | Noun))
# * The operator ⊗ should still be interpreted as addition +
# * The operator ⊕ is simplified and picks the minimum, that is, the path with lower overall weight: w1 ⊕ w2 = min(w1, w2) = { w1 if w1 < w2; w2 otherwise }
#
# Shown as a network with logprob weights in the tropical semiring:
#
# <img src="img/network_with_tropical_weights.png">
#
# #### Another example of weighted determinization in the tropical semiring
#
# <img src="img/weighted_determinization_example.png">

from hfst_dev import read_att_string
tr = read_att_string(
"""0 1 a a 0
0 1 b b 1
0 1 c c 4
0 2 a a 3
0 2 b b 4
0 2 c c 7
0 2 d d 0
0 2 e e 1
1 3 f f 1
1 3 e e 0
1 3 e e 2
2 3 e e 10
2 3 f f 11
2 3 f f 13
3 0
""")
print(tr)

tr.determinize()
print(tr)

# Weights must be pushed before minimization can take place:
#
# <img src="img/weight_pushing_and_minimization.png">

tr.minimize()
print(tr)

# #### Other uses
#
# Mehryar Mohri did not work on morphology, but on automatic speech recognition:
#
# <img src="img/speech_recognition.png">
#
# ## Further reading
#
# * To learn more, you can read the full article by Mohri et al. at: http://www.cs.nyu.edu/~mohri/pub/csl01.pdf
# * There are more similar articles, such as the version that was actually published in Computer Speech and Language in 2002.
# * Or look at the OpenFST library: http://www.cs.columbia.edu/~mohri/
