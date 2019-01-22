# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 3
#
# * (1.) Disambiguation
# * (2.) Probabilities, basics
# * (3.) Back to disambiguation
# * (4.) Spelling correction
# * (5.) Logprobs
# * (6.) Summary of types of finite-state automata and transducers
#
# ## 1. Disambiguation
#
# Some Finnish noun examples:
#
# * nainen
# * lautasilla
# * lautasilta
# * poikasilla
# * poikasilta
#
# The Finnish noun examples with analyses:
#
# * nainen 🡒 nainen +N +Sg +Nom (“woman”)
# * lautasilla 🡒 lautanen +N +Pl +Ade (“on plates”)
# * lautasilta 🡒 lautanen +N +Pl +Abl (“from plates”)
# * poikasilla 🡒 poikanen +N +Pl +Ade (“with cubs”)
# * poikasilta 🡒 poikanen +N +Pl +Abl (“from cubs”)
#
# The Finnish noun examples with more analyses:
#
# * nainen 🡒 naida +V +Pot +Pres +Sg1 (“it seems I’ll marry”)
# * lautasilla 🡒 lauta#silla +N +Sg +Ade (“board rayon”)
# * lautasilta:
#   - 🡒 lauta#silta +N +Sg +Nom (“board bridge”)
#   - 🡒 lautas#ilta +N +Sg +Nom (“plate evening”)
# *  poikasilla 🡒 poika#silla +N +Sg +Ade (“boy rayon”)
# *  poikasilta:
#   - 🡒 poika#silta +N +Sg +Nom (“boy bridge”)
#   - 🡒 poikas#ilta +N +Sg +Nom (“cub evening”)
#
# How disambiguate?
#
# * We could disambiguate (= find one unambiguous analysis) by looking at the word in context.
# * However, if we don’t have any context, we may still have a sense of which analyses are more likely _a priori_.
# * A priori = in general, without further information.
# * _A posteriori_, when we have more information, it may turn out that the most likely analysis a priori is not the correct one, but it is the best guess without more information.
#
# A priori assumptions:
#
# * "Nainen +N" is more common than "naida +V".
# * Singular (+Sg) is more common than Plural (+Pl).
# * Nominative (+Nom) is more common than the other cases.
# * Adessive (+Ade) is slightly more common than Ablative case (+Abl).
# * Single-stem words are more common than compound words.
#
# Model with probabilities
#
# <img src="img/model_with_probabilities.png">
#
# ## 2. Probabilities, basics
#
# What is probability?
#
# * Probability is the measure of the likelihood that an event will occur.
# * Probability is quantified as a number between 0 and 1
#   * 0 indicates impossibility
#   * 1 indicates certainty
#
# Objective probability
#
# * The most popular version of objective probability is frequentist probability.
# * Claims that the probability denotes the relative frequency of occurrence of an experiment's outcome.
# * The experiment is repeated many times.
# * This interpretation considers probability to be the relative frequency "in the long run" of outcomes.
# * Typical examples:
#   * throwing a dice (1, 2, 3, 4, 5, 6)
#   * throwing a coin ("heads or tails")
#
# Discrete probability distribution of outcome from throwing an unbiased six-sided die
#
# <img src="img/one_six_sided_die.png">
#
# Probability of mutually exclusive events 🡒 ADD probabilities together
#
# ```
# P(S = 1 or S = 2) =
# P(S = 1) + P (S = 2) =
# 1/6 + 1/6 =
# 2/6 =
# 1/3
# ```
#
# Probability of all possible events combined 🡒 The sum must be 1!
#
# ```
# P(S = 1 or S = 2  or S = 3 or
#   S = 4  or S = 5  or S = 6) =
# P(S = 1) + P (S = 2) + P (S = 3) +
#   P(S = 4) + P (S = 5) + P (S = 6) =
# 1/6 + 1/6 + 1/6 + 1/6 + 1/6 + 1/6 =
# 6/6 =
# 1
# ```
#
# Discrete probability distribution of outcome from throwing two unbiased six-sided dice
#
# <img src="img/two_six_sided_dice.png">
#
# Probability of independent events that co-occur 🡒 MULTIPLY probabilities together
#
# ```
# P(Sblack = 1 and Swhite = 1) =
# P(Sblack = 1) * P(Swhite = 1) =
# 1/6 * 1/6 =
# 1/36
# ```
# 
# Probability of mutually exclusive events 🡒 Involves both addition and multiplication
#
# ```
# P((Sblack = 5 and Swhite = 6) or (Sblack = 6 and Swhite = 5)) =
# P(Sblack = 5) * P(Swhite = 6) + P(Sblack = 6) * P(Swhite = 5) =
# 1/6 * 1/6 + 1/6 * 1/6 =
# 1/36 + 1/ 36 =
# 2/36 =
# 1/18
# ```
#
# For comparison: A continuous probability distribution
#
# <img src="img/continuous_probability_distribution.png">
#
# <i>Image from Wikipedia.</i>
#
# * The variables are here real-valued ("floats") rather than discrete categories ("ints").
# * We get a smooth curve for the probability distribution, such as this Gaussian curve, the so-called normal distribution.
#
# Subjective probability
#
# * The most popular version of subjective probability is Bayesian probability.
# * Rather than relative frequency in a series of experiments, subjectivists think of probabilities as degrees of belief.
# * "The price at which you would buy or sell a bet that pays 1 unit of utility (such as money) if an event occurs, and 0 if the event does not occur."
# * Examples:
#   * Is there life on Mars?
#   * Will Trump win the presidential election in the USA? (Now, we know he did.)
#   * Will it snow in Helsinki tomorrow?
#   * Given specific symptoms, does a patient have cancer?
#
# Prior and posterior probabilities
#
# * In Bayesian statistics, there are prior probabilities and posterior probabilities
#   * also called a priori and a posteriori probabilities
# * The prior probability states the general assumptions made in the model, such as:
#   * P("It snows in Helsinki in January")
# * The posterior probability is a product of two probabilities: the prior probability and a conditional probability, such as:
#   * P("It snows in Helsinki on 23 Jan 2018" | "It snows in Helsinki in January") * P("It snows in Helsinki in January")
#
# ## 3. Back to disambiguation
#
# The "poikasilla" ambiguity: 1) poikanen +N +Pl +Ade
#
# <img src="img/poikanen_n_pl_ade.png">
#
# Do the calculations
#
# ```
# Prob(poikanen +N +Pl +Ade)
# = Prob(+N) * Prob("poikanen") * Prob(+Pl) * Prob(+Ade)
# = 0.5 * 0.0001 * 0.3 * 0.05
# = 0.00000075
# = 7.5 * 10^-7
# ```
#
# The "poikasilla" ambiguity: 2) poika#silla +N +Sg +Nom
#
# <img src="img/poika_silla_n_sg_nom.png">
#
# Do the calculations:
#
# ```
# Prob(poika#silla +N +Sg +Nom)
# = Prob(+N) * Prob(“poika”) * Prob(Compound word) * Prob(“silla”) * Prob(+Sg) * Prob(+Nom)
# = 0.5 * 0.001 * 0.1 * 0.000001 * 0.6 * 0.55
# = 0.0000000000165
# = 1.65 * 10^-11
# ```
#
# Compare and pick the more likely alternative 🡒 The analysis `poikanen +N +Pl +Ade` is almost 50000 times more likely
# than `poika#silla +N +Sg +Nom` (in this invented model).
#
# Formulated in lexc format with weights (The syntax is correct, but don't do it exactly like this yet):
#
# ```
# Multichar_Symbols +N +Sg +Pl +Nom +Ade +Abl ^A ^I ^J ^K ^S ^T
# 
# LEXICON Root
# Nouns "weight: 0.5" ;
# Verbs "weight: 0.3" ;
# ...
# 
# LEXICON Nouns
# ilta:il^Ta          Number "weight: 0.0002" ;
# lauta:lau^Ta        Number "weight: 0.00001" ;
# lautanen:lauta^S    Number "weight: 0.0001" ;
# nainen:nai^S        Number "weight: 0.001" ;
# poika:po^J^Ka       Number "weight: 0.001" ;
# poikanen:poika^S    Number "weight: 0.0001" ;
# silla:silla         Number "weight: 0.000001" ;
# silta:sil^Ta        Number "weight: 0.0005" ;
# ...
# 
# LEXICON Number
# +Sg:0               Case "weight: 0.6" ;
# +Pl:^I              Case "weight: 0.3" ;
# #:0  Nouns "weight: 0.1" ; ! Back to collect more stems
# 
# LEXICON Case
# +Nom:0              # "weight: 0.55" ;
# +Ade:ll^A           # "weight: 0.05" ;
# ...
# ```
#
# ## 4. Spelling correction
#
# ### Virtual keyboard of a mobile device
#
# The D key was "pressed" (that is, touched).
#
# <img src="img/d_pressed.png">
#
# ### Noisy virtual keyboard of a mobile device
#
# The D key was "pressed" (that is, touched), but the intended key was actually F!
#
# <img src="img/f_intended.png">
#
# Assume probabilities:
#
# ```
# P(p = F | i = F) = 0.7
# P(p = D | i = F) = 0.1
# P(p = G | i = F) = 0.1
# P(p = R | i = F) = 0.025
# P(p = T | i = F) = 0.025
# P(p = C | i = F) = 0.025
# P(p = X | i = F) = 0.0125
# P(p = V | i = F) = 0.0125
# ```
#
# For instance, read the last line as: "The Probability that V was
# pressed when actually F was the intended key  is 0.0125."
#
# Create an FST that generates "noise" (errors) and invert it to get a spell checker
#
# <img src="img/spell_checker_model.png">
#
# ```
# Noisy surface 1:  poikasilla   (no error)
# Noisy surface 2:  loikasilla   (substitution)
# Noisy surface 3:  poikaslla    (deletion)
# Noisy surface 4:  ppoikasilla  (insertion)
# Noisy surface 5:  opikasilla   (transposition)
# ... etc
# ```
#
# xfst script snippet for a spell checker
#
# ```
# ! Use the .l operator to project only lower level (= surface forms) of the
# ! transducer; we are not interested in the upper level (= lexical forms)
# define Vocabulary [ Lexicon .o. AlternationRules ].l ;
# 
# ! Add "noise" (spelling errors); replace rules are optional when in brackets ()
# define Substitution  [ f (->) d::0.1 ] .o. [ f (->) g::0.1 ] .o.
#                      [ f (->) r::0.025 ] .o. [ f (->) t::0.025 ] .o.
#                      etc ... ;
# 
# ! Define a transducer from correctly spelled words to words containing errors
# define NoisyVocabulary  Vocabulary .o. Substitution ;
# 
# ! Use the .i operator to invert the transducer, such that the input is noisy
# ! words and the output is correctly spelled words
# define SpellChecker  [ NoisyVocabulary ].i ;
# 
# ! The spell checker is ready to use
# regex SpellChecker ;
# 
# ```
#
# Again, the syntax is correct, but there is something left to fix with the weights...
#
# ## 5. Logprobs
#
# Back to the probabilities
#
# We had the probability:
#
# ```
# Prob(poika#silla +N +Sg +Nom)
# = Prob(+N) * Prob("poika") * Prob(Compound word) * Prob("silla") * Prob(+Sg) * Prob(+Nom)
# = 0.5 * 0.001 * 0.1 * 0.000001 * 0.6 * 0.55
# = 0.0000000000165
# = 1.65 * 10^-11    
# ```
#
# This product of probabilities can be written as:
#
# ```
# This product of probabilities can be written as:
# (5 * 10^-1) * 10^-3 * 10^-1 * 10^-6 * (6 * 10^-1) * (5.5 * 10^-1)
# = 10^-0.301 * 10^-3 * 10^-1 * 10^-6 * 10^-0.222 * 10^-0.260
# = 10^-(0.301 + 3 + 1 + 6 + 0.222 + 0.260) =
# = 10^-10.783
# = 0.0000000000165
# ```
#
# If we agree on some base, such as 10, then instead of multiplying actual probabilities
# of co-occuring indendent events, we can add the (negative) exponents of the probabilities,
# which is faster and more manageable.
#
# Instead of `0.5 * 0.001 * 0.1 * 0.000001 * 0.6 * 0.55 = 0.0000000000165`,
# we get: `0.301 + 3 + 1 + 6 + 0.222 + 0.260 = 10.783`
#
# What we are doing is taking the negative logarithm of the probabilities:
# `10^-10.783 = 0.0000000000165` 🡒 `-log10 0.0000000000165 = 10.783`
#
# * A negative logarithm of a probability is called a _logprob_.
# * A logprob can be seen as a penalty term or a cost: "if you do this operation you'll have to pay this much."
# * Logprobs add up from operations performed in a sequence. 
# * If the probability of some operation is 1, that is, there is only one possible outcome:
#   * The logprob is `-log10 1 = 0`
#   * That is, there is no penalty if there is only one certain outcome.
#   * This makes sense.
#
# ### Weights in HFST
#
# * HFST does not really support probabilities as such.
# * HFST supports additive weights, such as logprobs.
# * Weights in lexc could look like:
#
# ```
# LEXICON Nouns
# ilta:il^Ta          Number "weight: 3.69897" ;
# lauta:lau^Ta        Number "weight: 5.00000" ;
# ...
# ```
#
# * Weights in xfst rules could look like:
#
# ```
# [ f (->) g::1.000 ] .o. [ f (->) r::1.602 ]
# ```
#
# ### Lexc with weights revisited
#
# <img src="img/lexc_with_weights_revisited.png">

from hfst_dev import compile_lexc_script

tr = compile_lexc_script("""
Multichar_Symbols +N +Sg +Pl +Nom +Ade +Abl ^A ^I ^J ^K ^S ^T 

LEXICON Root
           Nouns "weight: 0.30103" ;   ! Probability: 0.5
           Verbs "weight: 0.52288" ;   ! Probability: 0.3

LEXICON Nouns
ilta:il^Ta          Number "weight: 3.69897" ; ! Probability: 0.0002
lauta:lau^Ta        Number "weight: 5.00000" ; ! Probability: 0.00001
lautanen:lauta^S    Number "weight: 4.00000" ; ! Probability: 0.0001
nainen:nai^S        Number "weight: 3.00000" ; ! Probability: 0.001
poika:po^J^Ka       Number "weight: 3.00000" ; ! Probability: 0.001
poikanen:poika^S    Number "weight: 4.00000" ; ! Probability: 0.0001
silla:silla         Number "weight: 6.00000" ; ! Probability: 0.000001
silta:sil^Ta        Number "weight: 3.30103" ; ! Probability: 0.0005

LEXICON Number
+Sg:0               Case "weight: 0.22185" ;  ! Probability: 0.6
+Pl:^I              Case "weight: 0.52288" ;  ! Probability: 0.3
#:0  Nouns "weight: 1.00000" ; ! Back to collect more stems
                                              ! Probability: 0.1
LEXICON Case
+Nom:0              # "weight: 0.259637" ;    ! Probability: 0.55
+Ade:ll^A           # "weight: 1.301030" ;    ! Probability: 0.05

END
""")

# Invert and test the transducer:

tr.invert()
tr.minimize()
print(tr.lookup('poika^S^Ill^A'))
print(tr.lookup('poika^Sil^Ta'))
print(tr.lookup('po^J^Kasil^Ta'))

# ### Revisited xfst script for a spell checker
#
# <img src="img/xfst_with_weights_revisited.png">

from hfst_dev import compile_xfst_script
compile_xfst_script("""
! Toy example
define Lexicon {for}|{fight}|{right}|{tight}|{of}|{or} ;
define AlternationRules ?* ;

! Use the .l operator to project only lower level (= surface forms) of the 
! transducer; we are not interested in the upper level (= lexical forms)
define Vocabulary [ Lexicon .o. AlternationRules ].l ;

! Add "noise" (spelling errors); replace rules are optional when in brackets ()
define Substitution  [ f (->) d::1.000 ] .o. [ f (->) g::1.000 ] .o. 
                     [ f (->) r::1.602 ] .o. [ f (->) t::1.602 ] ; 
!                                                                .o. etc ... ;

! Define a transducer from correctly spelled words to words containing errors
define NoisyVocabulary  Vocabulary .o. Substitution ;

! Use the .i operator to invert the transducer, such that the input is noisy
! words and the output is correctly spelled words
define SpellChecker  [ NoisyVocabulary ].i ;

! The spell checker is ready to use
regex SpellChecker ;
invert net
minimize net
set print-weight ON

apply up right
echo --
apply up or
echo --
apply up for
""")

# ## 6. Summary of types of finite-state automata and transducers
#
# ### Finite-state automaton (FSA)
#
# A finite-state automaton (FSA) - or finite automaton - is a network consisting of nodes,
# which represent states, and directed arcs connecting the states,
# which represent transitions between states.
# Every arc is labeled with a symbol that is consumed from input.
# State transitions can also take place without consuming any input;
# these transitions are called epsilon transitions.
#
# <img src="img/fsa.png">

# TODO: use graphviz package

# HfstIterableTransducer is a special class for generating transducers
# from scratch or iterating them state by state and transition by transition.
# It does not support most of the ordinary transducer functions.
from hfst_dev import HfstIterableTransducer, EPSILON

tr = HfstIterableTransducer()
tr.add_transition(0, 1, EPSILON, EPSILON, 0)
tr.add_transition(0, 2, EPSILON, EPSILON, 0)
tr.add_transition(1, 3, 'b', 'b', 0)
tr.add_transition(2, 1, EPSILON, EPSILON, 0)
tr.add_transition(2, 2, 'b', 'b', 0)
tr.add_transition(3, 3, 'b', 'b', 0)
tr.add_transition(3, 4, EPSILON, EPSILON, 0)
tr.add_transition(3, 4, 'c', 'c', 0)
tr.set_final_weight(4, 0)

# Print the transducer in AT&T format:
print(tr)

# ### Weighted finite-state automaton (WFSA)
#
# A weighted finite-state automaton (WFSA) is an FSA with weights on the arcs.
# Weights make it possible to find the best way “through" an automaton for the given input;
# you want to take the path with the lowest weight.
#
# <img src="img/wfsa.png">

tr = HfstIterableTransducer()
tr.add_transition(0, 1, 'a', 'a', 2.7002)
tr.add_transition(0, 2, 'b', 'b', 1.0)
tr.add_transition(1, 1, 'a', 'a', 1.0)
tr.add_transition(1, 2, 'b', 'b', 0)
tr.add_transition(2, 2, 'b', 'b', 0.59961)
tr.add_transition(2, 3, 'c', 'c', 0)
tr.set_final_weight(2, 0)
tr.set_final_weight(3, 1.0)
print(tr)

# Weighted automata can be used to decide between two alternatives.
# For example, you’re running a speech recognition system and the user says "I have to go."
# How do you know the user didn’t say, "I have two go"?
# First, you come up with a probability of words occurring next to each other
# (for example, P("to go") and P("two go")) - a language model.
# Then, you translate those probabilities into weights for your finite state machine.
# Then, when you’re deciding between "to" and "two," you pick the sentence with lower weight ("to").
#
# ### Finite-state transducer (FST)
#
# A finite-state transducer (FST) is a finite automaton for which
# each transition has an input label and an output label.
#
# <img src="img/fst.png">
#
# It recognizes whether the two strings are valid correspondences (or translations)
# of each other.

tr = HfstIterableTransducer()
tr.add_transition(0, 1, 'a', 'a', 0)
tr.add_transition(1, 2, 'b', 'b', 0)
tr.add_transition(1, 3, 'a', 'a', 0)
tr.add_transition(2, 1, 'b', 'c', 0)
tr.add_transition(2, 3, 'a', 'a', 0)
tr.set_final_weight(3, 0)
print(tr)

# ### Weighted finite-state transducer (WFST)
#
# A weighted finite-state transducer (WFST) is a finite automaton for which
# each transition has an input label, an output label, and a weight.
#
# <img src="img/wfst.png">
#
# The initial state is labeled 0. The final state is 2 with final weight of 3.5.
# Any state with non-infinite final weight is a final state. There is a transition
# from state 0 to 1 with input label a, output label x, and weight 0.5.
# This machine transduces, for instance, the string "ac" to "xz" with weight 6.5
# (the sum of the arc and final weights).

tr = HfstIterableTransducer()
tr.add_transition(0, 1, 'a', 'x', 0.5)
tr.add_transition(0, 1, 'b', 'y', 1.5)
tr.add_transition(1, 2, 'c', 'z', 2.5)
tr.set_final_weight(2, 3.5)
print(tr)

# Convert to HfstTransducer before lookup.
from hfst_dev import HfstTransducer
TR = HfstTransducer(tr)
print(TR.lookup('ac'))

# ## More information
#
# * The Beesley & Karttunen book does not cover weighted finite-state machines. Weights were fairly new at about the time when the book was published in 2003.
# * HFST: [Using weights](https://github.com/hfst/python-hfst-4.0/wiki/Weights)
# * HFST [ospell](https://github.com/hfst/hfst-ospell/wiki)
