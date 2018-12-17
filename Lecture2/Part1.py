# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 2
#
# ## 1. Finite-State Basics
#
# Recall the finite-state transducer (FST) for purely concatenative I&A (Item and Arrangement)
# English noun inflection from Lecture 1:
#
# <img src="img/noun_inflection.png">
#
# The yellow circles represent _states_ or _nodes_ and the arrows represent _transitions_
# or _arcs_ between states. Each transition consumes an input symbol and produces an output symbol.
# The special symbol ε (the epsilon) on the input side means that no symbol is consumed
# and on the output side that no symbol is produced when following a given transition.
#
# A finite-state network that has only input symbols in the transitions is called
# a finite-state automaton (FSA). It does not produce output, but just recognizes
# (or rejects) input. Finite-state automaton for a 3-word language:
#
# <img src="img/three_word_language.png">
#
# * Inputs to the automaton are _symbols_ like: m, e, c.
# * The set of valid symbols that the automaton will accept is its _alphabet_: { a, c, e, g, i, m, n, o, r, s, t }.
# * The sequences of symbols that the automaton will accept are _words_ like: canto, mesa.
# * The entire set of words that the automaton accepts or recognizes is its _language_: { canto, mesa, tigre }.
#
# Sharing structure in minimal networks:
#
# <img src="img/fat_father.png">
#
# <img src="img/clear_clever_ear_ever.png">
#
# Removing a word from a minimal network may actually increase the size of the network!
#
# <img src="img/clear_clever_ever.png">
#
# ## 2. Set Theory for Finite-State Networks
#
# Examples of sets:
#
# <img src="img/two_sets.png">
#
# <img src="img/empty_set.png">
#
# Some sets viewed as networks:
#
# <img src="img/empty_network.png">
#
# <img src="img/empty_string_network.png">
#
# Some infinite sets:
#
# <img src="img/zero_or_more_a.png">
#
# <img src="img/universal_language.png">
#
# Relations:
#
# <img src="img/lowercase2uppercase.png">
#
# The example above shows an infinite relation containing pairs, such as
# `{<"dog","DOG">,<"cat","CAT">,<"mouse","MOUSE">,...}`
#
# We can also have relations between lexical forms and surface forms, such as:
# ```
# {<"cantar+Verb+PresInd+1P+Sg", "canto">,
#  <"cantar+Verb+PresInd+1P+Pl","cantamos">,
#  <"canto+Noun+Masc+Sg","canto">, ...}
#
# ```
#
# Union of sets
#
# <img src="img/union_of_sets.png">
#
# For instance, the union of the sets `{"clear", "clever", "ear", "ever"}` and `{"fat", "father"}` is
# `{"clear", "clever", "ear", "ever", "fat", "father"}`.
#
# The union shown as a network:
#
# <img src="img/union_of_sets_as_network.png">
#
# Intersection of sets
#
# <img src="img/intersection_of_sets.png">
#
# For instance, the intersection of sets `{}` and `{}` is `{}`
#
# Subtraction of one set from another
#
# <img src="img/subtraction_of_sets.png">
#
# For instance, the subtraction of sets `{}` and `{}` is `{}`
#
# Concatenation of sets
#
# <img src="img/concatenation_of_sets.png">
#
# Composition of transducers
#
# <img src="img/composition.png">
#
# Projection
#
# * Projection is extracting one side of a relation.
# * The upper projection of `<"cat", "CHAT">` is "cat".
# * The lower projection of `<"cat", "CHAT">` is "CHAT".
#
# <img src="img/projection.png">
#
# ### Set operations expressed in the xfst language
#
# ```
# [ A | B ] denotes the union of the two languages or relations A and B ("or"-operation).
# [ A & B ] denotes the intersection ("and"-operation).
# [ A - B ] denotes the subtraction of B from A.
# [ A B ] denotes the concatenation.
# [ A .o. B ] denotes the composition of the relations.
# A.u denotes the upper (i.e. input) projection.
# A.l denotes the lower (o.e. output) projection.
# ```
#
# ## 3. Item & Process morphology using xfst rules
#
# Recall the finite-state transducer for purely concatenative I&A English
# noun inflection (from previous lecture):
#
# <img src="img/noun_inflection.png">
#
# A more compact finite-state transducer for I&P English noun inflection:
#
# <img src="img/noun_inflection_compact.png">
#
# ### Cascade of transducers: Rule 1
#
# Insert 'e' after the end of the stem in front of 's', if the stem ends in
# 's', 'x', 'ch', 'sh' or 'y'.
#
# Expressed as an xfst rule:
#
# `define InsertE   [. .] -> e || [ s | x | c h | s h | y ] %^ _ s ;`
#
# <img src="img/InsertE.png">

from hfst_dev import regex, HfstTransducer

InsertE = regex("[. .] -> e || [ s | x | c h | s h | y ] %^ _ s")
print(InsertE.lookup("sky^s'"))

# ### Cascade of transducers: Rule 2
#
# Rewrite 'y' as 'i' when followed by the end of the stem, which is
# further followed by 'e'.
#
# Expressed as an xfst rule:
#
# `define YToI    y -> i || _ %^ e ;`
#
# <img src="img/YToI.png">

YToI = regex("y -> i || _ %^ e")
print(YToI.lookup("sky^es'"))

# ### Cascade of transducers: Rule 3
#
# Remove the end of stem marker
#
# Expressed as an xfst rule:
#
# `define CleanUp    %^ -> 0 ;`

CleanUp = regex("%^ -> 0")
print(CleanUp.lookup("ski^es'"))

# <img src="img/CleanUp.png">
#
# ### Cascade equivalent to single FST
#
# <img src="img/cascade.png">

from hfst_dev import compile_lexc_file
lexicon = compile_lexc_file('en_ia_morphology.lexc')

from hfst_dev import compose
cascade = compose((lexicon, InsertE, YToI, CleanUp))

# When our lexicon is composed with our rules, we can actually produce one
# single FST and 'jump' from the lexical-form input straight to the final
# output in one go, without producing the intermediate steps.
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

print(cascade.lookup("sky+N+Pl+Poss"))

# ### The order of the rules matters!
#
# What would happen if we reordered the rules (below) used in our simple
# English noun morphology?

cascade = compose((lexicon,YToI, InsertE, CleanUp))
print(cascade.lookup("sky+N+Pl+Poss"))

# ### xfst notation explained in context
#
# <img src="img/xfst_notation_explained_1.png">
#
# <img src="img/xfst_notation_explained_2.png">
#
# <img src="img/xfst_notation_explained_3.png">
#
# <img src="img/xfst_notation_explained_4.png">
#
# <img src="img/xfst_notation_explained_5.png">
#
# ## 4. Example: English adjectives
#
# ### Lexicon (lexc) of some English adjectives
#
# en_ip_adjectives_lexicon.lexc
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
# ### Suggested xfst script for English adjectives
#

from hfst_dev import compile_xfst_script

adj_lexicon = compile_xfst_script("""
! Read lexicon and make a regex of it
read lexc en_ip_adjectives_lexicon.lexc
define Lexicon ;
regex Lexicon ;

! y/i alternation
define YToI     y -> i || _ %^ e ;

! Last rule cleans away the boundary marker
define CleanUp  %^ -> 0 ;

! Compose lexicon with rules
regex Lexicon .o. YToI .o. CleanUp ;

! Output all surface forms of the words
lower-words 
""")

# There are issues with some word forms...
#
# ```
# big         biger       bigest
# cool        cooler      coolest
# crazy       crazier     craziest
# great       greater     greatest
# grim        grimer      grimest
# happy       happier     happiest
# hot         hoter       hotest
# long        longer      longest
# quick       quicker     quickest
# sad         sader       sadest
# short       shorter     shortest
# slow        slower      slowest
# small       smaller     smallest
# warm        warmer      warmest
# ```
#
# ### Corrected xfst script for English adjectives
#

adj_lexicon = compile_xfst_script("""
! Read lexicon and make a regex of it
read lexc en_ip_adjectives_lexicon.lexc
define Lexicon ;
regex Lexicon ;

define Vowel [ a | e | i | o | u | y ] ;
define Cons  [ b | c | d | f | g | h | j | k | l | m |
n | p | q | r | s | t | v | w | x | z ] ;

! y/i alternation
define YToI     y -> i || _ %^ e ;

! Consonant reduplication
define DoubleCons d -> d d ,
g -> g g ,
m -> m m ,
t -> t t || Cons Vowel _ %^ e ;

! Last rule cleans away the boundary marker
define CleanUp  %^ -> 0 ;

! Compose lexicon with rules
regex Lexicon .o. YToI .o. DoubleCons .o. CleanUp ;

! Output all surface forms of the words
lower-words 
""")

# Now it works!
#
# ```
# big        bigger      biggest
# cool       cooler      coolest
# crazy      crazier     craziest
# great      greater     greatest
# grim       grimmer     grimmest
# happy      happier     happiest
# hot        hotter      hottest
# long       longer      longest
# quick      quicker     quickest
# sad        sadder      saddest
# short      shorter     shortest
# slow       slower      slowest
# small      smaller     smallest
# warm       warmer      warmest
# ```
#
# More information
#
# * Chapter 1 of the Beesley & Karttunen book: "A Gentle Introduction"
# * Chapter 3 of the Beesley & Karttunen book: "The xfst Interface"
#
