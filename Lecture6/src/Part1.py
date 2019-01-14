# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 6
#
# ## 1. Two-level rules
#
# Recall the finite-state transducer for I&P English noun inflection (from lecture 1):
#
# <img src="img/noun_inflection.png">
#
# ```
# Example input:    ∅sky+N+Pl+Poss
# Example output:   ∅sky^  s  '
# ```
# 
# Xfst rules are placed in a series.
# We compose our lexicon with our rewrite rules (called “replace rules” in xfst)
# and  produce one single FST that “jumps” from the lexical-form input straight to
# the final output in one go, without producing the intermediate steps.
#
# <img src="img/cascade.png">
#
# ```
# Example input:  sky+N+Pl+Poss
# Lexicon output: sky^s'
# Rule 1 output:  sky^es
# Rule 2 output:  ski^es
# Rule 3 output:  skies
# ```
#
# The single FST will give directly: sky+N+Pl+Poss 🡒 skies.
# 
# The order of the rules matters!
#
# 

