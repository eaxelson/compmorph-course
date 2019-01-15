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
# <img src="img/xfst_and_twolc_scripts.png">
#
# Which one to use is mostly a matter of taste. The xfst syntax allows lexicon to be read from file
# and composed with the rules. In twolc, this must be done by hand(?). Compare the following:

from hfst_dev import compile_xfst_file, compile_twolc_file, compile_lexc_file
from hfst_dev import intersect, compose, HfstTransducer

# The xfst script reads en_ip_adjectives_lexicon.lexc, composes it
# with the xfst rules, and stores the result to en_adjectives.xfst.hfst.
compile_xfst_file('en_adjectives.xfst')
xfst = HfstTransducer.read_from_file('en_adjectives.xfst.hfst')
print(xfst.lookup('big+A+Pos'))

# Explicitely compile the lexicon.
lexicon = compile_lexc_file('en_ip_adjectives_lexicon.lexc')
# Compile the twolc file and store the result to en_adjectives.twolc.hfst.
compile_twolc_file('en_adjectives.twolc', 'en_adjectives.twolc.hfst')
# Read the rules from file,
twolc_rules = HfstTransducer.read_all_from_file('en_adjectives.twolc.hfst')
# intersect them (not compose!),
twolc_rule = intersect(twolc_rules)
# and the lexicon with them.
twolc = compose((lexicon, twolc_rule))
print(twolc.lookup('big+A+Pos'))

# The results should be the same.
assert(twolc.compare(xfst))

# ## 3. Twol rule operators
#
# twolc rule operators
#
# <img src="img/twolc_rule_operators.png">
#
# Examples of twolc operators in context
#
# <img src="img/twolc_rule_operator_examples.png">
#
# Resolving conflicting rules
#
# <img src="img/resolving_conflicting_rules.png">

compile_twolc_file('conflicting_rules.twolc', 'conflicting_rules.twolc.hfst')
twolc_rules = HfstTransducer.read_all_from_file('conflicting_rules.twolc.hfst')
twolc = intersect(twolc_rules)
print(twolc.lookup('rar'))
print(twolc.lookup('lar'))

# Expect the result:
# ```
# rar: (('rbr', 0.0),)
# lar: (('lcr', 0.0),)
# ```

# ## 4. Example: consonant gradation in English
#
# Examples taken from From: Karttunen & Beesley (1992): Two-Level Rule Compiler. http://www.cis.upenn.edu/~cis639/docs/twolc.html.
#
# Consonant gradation in Finnish
#
# <img src="img/consonant_gradation_in_finnish.png"> 
#
# Two-level grammar for consonant gradation
#
# <img src="img/consonant_gradation_twolc.png">
#
# More information
#
# * Unpublished chapter of Beesley & Karttunen (2003): “Two-Level Rule Compiler”: http://web.stanford.edu/~laurik/.book2software/twolc.pdf
# * Karttunen & Beesley (1992): Two-Level Rule Compiler. Technical Report. ISTL-92-2. Xerox Palo Alto Research Center, California. http://www.cis.upenn.edu/~cis639/docs/twolc.html
# * HFST: Tutorial hfst-lexc and hfst-twolc: TODO
#
