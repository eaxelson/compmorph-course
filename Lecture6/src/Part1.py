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
# Two-level morphology is different
#
# <img src="img/series.png">
#
# * The order of the rules does not matter
# * The rule transducers are combined by intersection rather than composition
#
# Compare rule declarations for xfst vs. twol:
#
# <img src="img/rule_declarations_compared.png">
#
# Some of the twol notation explained:
#
# <img src="img/twol_notation_explained.png">
#
# ## 2. Example: English adjectives
#
# Recall the lexicon (lexc) of some English adjectives from lecture 2:
#
# ```
# Multichar_Symbols
# +A       ! Adjective tag
# +Pos     ! Positive
# +Cmp     ! Comparative
# +Sup     ! Superlative
#
# LEXICON Root
# Adjectives ;
#
# LEXICON Adjectives
# big     A ;
# cool    A ;
# crazy   A ;
# great   A ;
# grim    A ;
# happy   A ;
# hot     A ;
# long    A ;
# quick   A ;
# sad     A ;
# short   A ;
# slow    A ;
# small   A ;
# warm    A ;
#
# LEXICON A
# +A:^    Comparison ;
#
# LEXICON Comparison
# +Pos:0  # ;
# +Cmp:er # ;
# +Sup:est  # ;
#
# END
# ```
#
# Also recall the corrected script (xfst) from Lecture 2 that is shown below with an equivalent script implemented with twolc:
#
# <img = "src/xfst_and_twolc_scripts.png">
#
# Which one to use is mostly a matter of taste.
#
# ## 3. Twol rule operators
#
# twolc rule operators
#
# <img src="twolc_rule_operators.png">
#
# Examples of twolc operators in context
#
# <img src="twolc_rule_operator_examples.png">
#
# Resolving conflicting rules
#
# <img src="resolving_conflicting_rules.png">
#
