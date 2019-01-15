# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 7
#
# ## 1. Flag diacritics
#
# Inflection of Arabic “kitaab” (= book):
#
# <img src="img/inflection_of_kitaab.png">
#
# Combinations of the definite article together with indefinite forms are not allowed, such as *alkitaabuN.
#
# Lexc file for the inflection of “kitaab”:
#
# ``` 
# Multichar_Symbols +Def +Indef +Nom +Acc +Gen
# 
# LEXICON Root
#         Nouns ;
# 
# LEXICON Nouns
# al      DefStems ;
#         DefStems ;
#         IndefStems ;
# 
# LEXICON DefStems
# kitaab  DefCase ;     ! add other stems here
# 
# LEXICON IndefStems
# kitaab  IndefCase ;   ! add other stems here
# 
# LEXICON DefCase
# +Def+Nom:u      # ;
# +Def+Acc:a      # ;
# +Def+Gen:i      # ;
# 
# LEXICON IndefCase
# +Indef+Nom:uN   # ;
# +Indef+Acc:aN   # ;
# +Indef+Gen:iN   # ;                      
# ```
#
# Any problems?
#
# Finite-state transducer of the “kitaab” lexc file:
#
# <img src="img/fst_of_kitaab.png">
#
# The long-distance dependency is encoded by the path taken for the stems.
#
# Lexc file for “kitaab” using flag diacritics for the definite form:
#
# ```
# Multichar_Symbols +Def +Indef +Nom +Acc +Gen
#                   @U.ART.PRESENT@ @U.ART.ABSENT@
# 
# LEXICON Root
#         Nouns ;
# 
# LEXICON Nouns
# al@U.ART.PRESENT@  Stems ;
#                    Stems ;
# 
# LEXICON Stems
# kitaab  Case ;   ! add other stems here
# 
# LEXICON Case
# +Def+Nom:u      # ;
# +Def+Acc:a      # ;
# +Def+Gen:i      # ;
# @U.ART.ABSENT@IndefCase ;
# 
# LEXICON IndefCase
# +Indef+Nom:uN   # ;
# +Indef+Acc:aN   # ;
# +Indef+Gen:iN   # ;                                             
# ```
#
# Finite-state transducer of the “kitaab” lexc file using flag diacritics for the definite form:
#
# <img src="img/fst_of_kitaab_with_flags.png">
#
# The long-distance dependency is encoded by flags that are stored in memory
# as we progress through the network.
#
# Lexc with “bi” article that governs the genitive case:
#
# ```
# Multichar_Symbols +Def +Indef +Nom +Acc +Gen
#                   @U.ART.PRESENT@ @U.ART.ABSENT@
#                   @U.CASE.NOM@ @U.CASE.ACC@ @U.CASE.GEN@
# 
# LEXICON Root
#         Preposition ;
# 
# LEXICON Preposition
# bi@U.CASE.GEN@  Article ; ! optional preposition prefix
#                 Article ; ! empty string entry
# 
# LEXICON Article
# al@U.ART.PRESENT@ Stems ; ! opt. def. article prefix
#                   Stems ; ! empty string entry
# 
# LEXICON Stems
# kitaab  Case ;            ! add other stems here
# 
# LEXICON Case
# +Def+Nom:u      MarkNOM ;
# +Def+Acc:a      MarkACC ;
# +Def+Gen:i      MarkGEN ;
# @U.ART.ABSENT@  IndefCase ;
#
# LEXICON IndefCase
# +Indef+Nom:uN   MarkNOM ;
# +Indef+Acc:aN   MarkACC ;
# +Indef+Gen:iN   MarkGEN ;
# 
# LEXICON MarkNOM
# @U.CASE.NOM@    # ;
# 
# LEXICON MarkACC
# @U.CASE.ACC@    # ;
# 
# LEXICON MarkGEN
# @U.CASE.GEN@    # ;
# ```
#
# Transducer with “bi” article governing the genitive case:
#
# <img src="img/fst_of_kitaab_genitive.png">
#
# Tricky lexc syntax when upper and lower forms are different:
#
# <img src="img/tricky_lexc_syntax.png">

# ### Full range of flag-diacritic operators
#
# * General format:
#   - `@operator.feature.value@`
#   - `@operator.feature@` (operates on the “neutral” = unset value)
# * The features and values can be (almost) any string you like; the strings are case sensitive, e.g., “DEFINITE” is not the same as “definite”.
# * The operator must be one of: `P`, `N`, `C`, `R`, `D`, `U`:
#
# <img src="img/flag_diacritic_operators.png">
#

# <img src="img/foo.png">
#

# ## 2. Non-concatenative morphotactics
#
# 
