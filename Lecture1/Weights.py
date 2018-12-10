# # Using weights
#
# Weights in transducers represent probabilities.
# The can be used e.g. in disambiguation and spelling correction.
# HFST supports weights in the tropical semiring, i.e.
# logarithmic probabilities that are interpreted as penalties/costs
# on a given path that is followed. In morphologies, weights can be defined
# both for lexical entries and rules.

# A simple example of disambiguation of Finnish morphology:
# The inflected form "lautasilta" has three possible analyses:
#
# * lautanen+N+Pl+Abl ("from plates")
# * lauta#silta+N+Sg+Nom ("board bridge")
# * lautas#ilta+N+Sg+Nom ("plate evening")
#
# If we don't have any context, we can use general rules:
#
# * Nominative (+Nom) is more common than the other cases.
# * Singular (+Sg) is more common than Plural (+Pl)
# * Single-stem words are more common than compound words.
# * Probabilities of individual words.
#
# Let's suppose the following probablilities (expressed both as Bayesian probabilities
# and logarithmic penalties/costs):
#
# ```
# lautanen  0.0001     4.0
# lauta     0.00001    5.0
# silta     0.0005     3.3
# ilta      0.0002     3.7
#
# +Sg       0.6        0.22
# +Pl       0.3        0.52
# #         0.1        1.0
#
# +Nom      0.55       0.26
# +Abl      0.05       1.3
# ```
#
# We can then construct a simple LexC script for the above case of Finnish morphology:

from hfst_dev import compile_lexc_script, HfstTransducer

tr = compile_lexc_script("""
Multichar_Symbols +N +Sg +Pl +Nom +Abl ^S ^T

LEXICON Root
        Nouns ;

LEXICON Nouns
lautanen:lauta^S  Noun "weight: 4.0" ;
lauta:lau^Ta      Noun "weight: 5.0" ;
silta:sil^Ta      Noun "weight: 3.3" ;
ilta:il^Ta        Noun "weight: 3.7" ;

LEXICON Noun
+N:0     Number ;
#:0      Nouns  "weight: 1.0" ;

LEXICON Number
+Sg:0    Case   "weight: 0.22" ;
+Pl:i    Case   "weight: 0.52" ;

LEXICON Case
+Nom:0    #  "weight: 0.26" ;
+Abl:lta  #  "weight: 0.05" ;

END
""")

print(tr.lookup('lautanen+N+Pl+Abl'))
print(tr.lookup('lauta#silta+N+Sg+Nom'))
print(tr.lookup('lautanen#ilta+N+Sg+Nom'))

# Probablities of "lauta#silta+N+Sg+Nom'" and "lautanen#ilta+N+Sg+Nom" are almost the same,
# because we have no semantic information in our simple model.
