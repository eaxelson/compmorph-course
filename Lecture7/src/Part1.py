# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 7
#
# <ul>
#  <li>1. <a href="#1.-Flag-diacritics">Flag diacritics</a></li>
#  <li>2. <a href="#2.-Non-concatenative-morphotactics">Non-concatenative morphotactics</a></li>
# </ul>
#
# ## 1. Flag diacritics
#
# ### 1.1. The approach without flag diacritics
#
# Inflection of Arabic "kitaab" (= book):
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
# #### Finite-state transducer of the “kitaab” lexc file:
#
# <img src="img/fst_of_kitaab.png">
#
# The long-distance dependency is encoded by the path taken for the stems.
#
# ### 1.2. Using flag diacritics
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
# #### Finite-state transducer of the “kitaab” lexc file using flag diacritics for the definite form:
#
# <img src="img/fst_of_kitaab_with_flags.png">
#
# The long-distance dependency is encoded by flags that are stored in memory
# as we progress through the network.

from hfst_dev import compile_lexc_script
tr = compile_lexc_script("""
Multichar_Symbols +Def +Indef +Nom +Acc +Gen
                  @U.ART.PRESENT@ @U.ART.ABSENT@
 
LEXICON Root
        Nouns ;
 
LEXICON Nouns
al@U.ART.PRESENT@  Stems ;
                   Stems ;

LEXICON Stems
kitaab  Case ;   ! add other stems here
 
LEXICON Case
+Def+Nom:u      # ;
+Def+Acc:a      # ;
+Def+Gen:i      # ;
@U.ART.ABSENT@IndefCase ;
 
LEXICON IndefCase
+Indef+Nom:uN   # ;
+Indef+Acc:aN   # ;
+Indef+Gen:iN   # ;                                             
""")
print(tr.lookup('alkitaab+Def+Gen'))
tr.invert()
print(tr.lookup('alkitaabi'))


# #### Adding the genitive case
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
# #### Transducer with “bi” article governing the genitive case:
#
# <img src="img/fst_of_kitaab_genitive.png">

tr = compile_lexc_script("""
Multichar_Symbols +Def +Indef +Nom +Acc +Gen
                  @U.ART.PRESENT@ @U.ART.ABSENT@
                  @U.CASE.NOM@ @U.CASE.ACC@ @U.CASE.GEN@

LEXICON Root
        Preposition ;

LEXICON Preposition
bi@U.CASE.GEN@  Article ; ! optional preposition prefix
                Article ; ! empty string entry

LEXICON Article
al@U.ART.PRESENT@ Stems ; ! opt. def. article prefix
                  Stems ; ! empty string entry

LEXICON Stems
kitaab  Case ;            ! add other stems here

LEXICON Case
+Def+Nom:u      MarkNOM ;
+Def+Acc:a      MarkACC ;
+Def+Gen:i      MarkGEN ;
@U.ART.ABSENT@  IndefCase ;

LEXICON IndefCase
+Indef+Nom:uN   MarkNOM ;
+Indef+Acc:aN   MarkACC ;
+Indef+Gen:iN   MarkGEN ;

LEXICON MarkNOM
@U.CASE.NOM@    # ;

LEXICON MarkACC
@U.CASE.ACC@    # ;

LEXICON MarkGEN
@U.CASE.GEN@    # ;
""")
print(tr.lookup('bikitaab+Def+Gen'))
tr.invert()
print(tr.lookup('bikitaabi'))

# #### Tricky lexc syntax when upper and lower forms are different:
#
# <img src="img/tricky_lexc_syntax.png">

# ### 1.3. Full range of flag-diacritic operators
#
# <ul>
# <li>General format:</li>
#   <ul>
#    <li><code>@operator.feature.value@</code></li>
#    <li><code>@operator.feature@</code> (operates on the “neutral” = unset value)</li>
#   </ul>
#  <li>The features and values can be (almost) any string you like; the strings are case sensitive, e.g., “DEFINITE” is not the same as “definite”.</li>
#  <li>The operator must be one of: <code>{P, N, C, R, D, U}</code></li>
# </ul>
#
# <img src="img/flag_diacritic_operators.png">
#
# #### P flag: positive (re)setting
#
# <ul>
# <li>Example:</li>
#  <ul>
#   <li><code>@P.CASE.GEN@</code></li>
#   <li>Set the value of <code>CASE</code> to <code>GEN</code></li>
#   <li>It does not matter what <code>CASE</code> was before, or if it was set at all</li>
#   <li>Never fails</li>
#  </ul>
# </ul>
#
# #### N flag: negative (re)setting
#
# <ul>
# <li>Example: <code>@N.CASE.GEN@</code></li>
#  <ul>
#   <li>Set the value of <code>CASE</code> to something other than <code>GEN</code></li>
#   <li>The value of <code>CASE</code> is not well defined after this, but there is some value and we know it is not <code>GEN</code></li>
#   <li>It does not matter what <code>CASE</code> was before, or if it was set at all</li>
#   <li>Never fails</li>
#  </ul>
# </ul>
#
# #### C flag: clear feature
#
# <ul>
# <li>Example: <code>@C.CASE@</code></li>
#  <ul>
#   <li>Unset the value of <code>CASE</code></li>
#   <li><code>CASE</code> has no value after this (also called neutral)</li>
#   <li>It does not matter what <code>CASE</code> was before, or if it was set at all</li>
#   <li>Never fails</li>
#  </ul>
# </ul>
#
# #### R flag: require test
#
# <ul>
# <li>Examples:</li>
#  <ul>
#   <li><code>@R.CASE.GEN@</code></li>
#     <ul>
#      <li>Succeeds if <code>CASE</code> has the value <code>GEN</code></li>
#      <li>Otherwise fails and blocks this path</li>
#      <li>Does not set or modify the value of <code>CASE</code></li>
#     </ul>
#   <li><code>@R.CASE@</code></li>
#    <ul>
#     <li>Succeeds if <code>CASE</code> is set to some value (not neutral)</li>
#     <li>Otherwise fails and blocks this path</li>
#     <li>Does not set or modify the value of <code>CASE</code></li>
#    </ul>
#  </ul>
# </ul>
#
# #### D flag: disallow test
#
# <ul>
# <li>Examples:</li>
#  <ul>
#   <li><code>@D.CASE.GEN@</code>
#    <ul>
#     <li>Succeeds if <code>CASE</code> does not have the value <code>GEN</code></li>
#     <li>Otherwise fails and blocks this path</li>
#     <li>Does not set or modify the value of <code>CASE</code></li>
#    </ul>
#   <li><code>@D.CASE@</code>
#    <ul>
#     <li>Succeeds if <code>CASE</code> is not set to any value (neutral)</li>
#     <li>Otherwise fails and blocks this path</li>
#     <li>Does not set or modify the value of <code>CASE</code></li>
#   </ul>
#  </ul>
# </ul>
#
# #### U flag: unification test
#
# <ul>
# <li>Examples:</li>
#  <ul>
#   <li><code>@U.CASE.GEN@</code></li>
#    <ul>
#     <li>Succeeds if <code>CASE</code> has the value <code>GEN</code></li>
#     <li>Also succeeds if <code>CASE</code> is unset (neutral); in this instance, <code>CASE</code> is set to <code>GEN</code> after this operation</li>
#     <li>Otherwise fails and blocks this path</li>
#    </ul>
#   <li><code>al@U.ART.PRESENT@kitaab@U.ART.ABSENT@uN@U.CASE.NOM@</code></li>
#    <ul>
#     <li>Fails</li>
#    </ul>
#   <li><code>bi@P.CASE.GEN@al@U.ART.PRESENT@kitaabi@U.CASE.GEN@</code></li>
#    <ul>
#     <li>Succeeds</li>
#   </ul>
#  </ul>
# </ul>

from hfst_dev import regex

failing = regex('@U.ART.PRESENT@')
print(failing)

# note that '@' has a special meaning in regular expressions, so it must be quoted to be interpreted literally
fails = regex('al"@U.ART.PRESENT@"kitaab"@U.ART.ABSENT@"uN"@U.CASE.NOM@"')
print(fails.lookup('alkitaabuN'))

succeeds = regex('bi"@P.CASE.GEN@"al"@U.ART.PRESENT@"kitaabi"@U.CASE.GEN@"')
print(succeeds.lookup('bialkitaabi'))

# ### 1.4. More examples with the same flag-diacritic operators
#
# <img src="img/n_foo_blah.png">
#
# <i>Image from Beesley & Karttunen: Finite State Morphology (2003).</i>
#
# <ul>
#  <li><code>@P.FEAT.M@</code> <code>@D.FEAT.M@</code> will fail.</li>
#  <li><code>@N.FEAT.M@</code> <code>@D.FEAT.Q@</code> will fail.</li>
#  <li><code>@R.FEAT@</code> will succeed if <code>FEAT</code> is currently set to some other value than neutral.</li>
#  <li><code>@U.FEAT.M@</code> succeeds if <code>FEAT</code> is currently set to <code>M</code> or neutral; the value is reset to <code>M</code> after this operation.</li>
#  <li><code>@N.FEAT.M@</code> <code>@U.FEAT.Q@</code> succeeds, leaving <code>FEAT=Q</code> in memory.</li>
# </ul>

# ## 2. Non-concatenative morphotactics
#
# ### 2.1. Limited reduplication in Tagalog verbs
#
# <img src="img/tagalog_verbs.png">
#
# ### 2.2. Full-stem reduplication in Malay nouns
#
# <img src="img/malay_nouns.png">
#
# ### 2.3. Arabic word forms based on roots d-r-s and k-t-b
#
# <img src="img/arabic_word_forms.png">
#
# ### 2.4. Tagalog limited reduplication: easy with two-level morphology!
#
# <img src="img/tagalog_reduplication.png">

from hfst_dev import compile_lexc_file, compile_twolc_file, HfstTransducer, intersect, compose
lexc = compile_lexc_file('tagalog.lexc')
compile_twolc_file('tagalog.twolc', 'tagalog.twolc.hfst')
twolc_rules = HfstTransducer.read_all_from_file('tagalog.twolc.hfst')
twolc = intersect(twolc_rules)
tagalog = compose((lexc, twolc))
print(tagalog.lookup('RE+pili'))

# ### 2.5. Malay full-stem reduplication with compile-replace
#
# <img src="img/malay_reduplication.png">

from hfst_dev import compile_xfst_file
compile_xfst_file('malay.xfst')
xfst = HfstTransducer.read_from_file('malay.xfst.hfst')
print(xfst.lookup('buku+Noun+Plural'))

# ### 2.6. Arabic “morphemes”
#
# <img src="img/arabic_morphemes.png">
#
# <i>Image from Beesley & Karttunen: Finite State Morphology (2003).</i>
#
# #### Arabic morphotactics using merge and compile-replace
#
# <ul>
#  <li>xfst operator for merge to the right: <code>.m&gt;.</code></li>
#  <li>xfst operator for merge to the left: <code>.&lt;m.</code></li>
#  <li>For instance,</li>
#   <ul>
#    <li>Lexical form: <code>[ ktb     +FormI     +Pass] +3P+Fem+Sg</code></li>
#    <li>Surface form: <code>^[{ktb}.m&gt;.{CVCVC}.&lt;m.[u*i]^]at</code></li>
#   </ul>
#  <li>The compile-replace algorithm executes the merge commands in the regular expression and produces the final surface form: <code>kutibat</code></li>
# </ul>
#
# #### Arabic morphotactics with Twol regular expression center rules
#
# <img src="img/arabic_morphotactics.png">

lexc = compile_lexc_file('arabic.lexc')
# todo: unresolvable conflicting rules
compile_twolc_file('arabic.twolc', 'arabic.twolc.hfst')
twolc_rules = HfstTransducer.read_all_from_file('arabic.twolc.hfst')
twolc = intersect(twolc_rules)
arabic = compose((lexc, twolc))
print(arabic.lookup('[ktb+FormI+Pass]+3P+Fem+Sg'))

# ## More information
#
# <ul>
#  <li>Chapter 7 of the Beesley & Karttunen book: “Flag Diacritics”</li>
#  <li>Chapter 8 of the Beesley & Karttunen book: “Non-Concatenative Morphotactics”</li>
#  <li>HFST: <a href="https://github.com/hfst/hfst/wiki/HfstTwolc">hfst-twolc command line tool</a></li>
# </ul>
