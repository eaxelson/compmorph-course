# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 3
#
# ## Section 1: Disambiguation
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
# * nainen => nainen +N +Sg +Nom (“woman”)
# * lautasilla => lautanen +N +Pl +Ade (“on plates”)
# * lautasilta => lautanen +N +Pl +Abl (“from plates”)
# * poikasilla => poikanen +N +Pl +Ade (“with cubs”)
# * poikasilta => poikanen +N +Pl +Abl (“from cubs”)
#
# The Finnish noun examples with more analyses:
#
# * nainen => naida +V +Pot +Pres +Sg1 (“it seems I’ll marry”)
# * lautasilla => lauta#silla +N +Sg +Ade (“board rayon”)
# * lautasilta => lauta#silta +N +Sg +Nom (“board bridge”)
# *            => lautas#ilta +N +Sg +Nom (“plate evening”)
# *  poikasilla => poika#silla +N +Sg +Ade (“boy rayon”)
# *  poikasilta => poika#silta +N +Sg +Nom (“boy bridge”)
# *             => poikas#ilta +N +Sg +Nom (“cub evening”)
#
# How disambiguate?
#
# * We could disambiguate (= find one unambiguous analysis) by looking at the word in context.
# * However, if we don’t have any context, we may still have a sense of which analyses are more likely a priori.
# * A priori = in general, without further information.
# * A posteriori, when we have more information, it may turn out that the most likely analysis a priori is not the correct one, but it is the best guess without more information.
#
# A priori assumptions
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
# ## Section 2: Probabilities, basics
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
#   * Will it snow in Helsinki tomorrow (23 January 2018)?
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
# ## Section 3: Back to disambiguation
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
# <img src="poika_silla_n_sg_nom.png">
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
# Compare and pick the more likely alternative 🡒 The analysis "poikanen +N +Pl +Ade" is almost 50000 times more likely
# than #poika#silla +N +Sg +Nom# (in this invented model).
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
# ## Section 4: Spelling correction
#
# Virtual keyboard of a mobile device
#
# The D key was "pressed" (that is, touched).
#
# <img src="img/d_pressed.png">
#
# Noisy virtual keyboard of a mobile device
#
# The D key was "pressed" (that is, touched), but the intended key was actually F!
#
# <img src="img/f_intended.png">
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
# ## Section 5: Logprobs
#
# 
#
# ## Section 6: Summary of types of finite-state automata and transducers
#
# <img src="img/fsa.png">
#
# <img src="img/wfsa.png">
#
# <img src="img/fst.png">
#
# <img src="img/wfst.png">
#
# ## More information
#
# * The Beesley & Karttunen book does not cover weighted finite-state machines. Weights were fairly new at about the time when the book was published in 2003.
# * HFST: [Using weights]()
# * HFST [ospell]()
