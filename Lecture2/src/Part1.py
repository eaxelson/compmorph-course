# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 2
#
# <ul>
# <li>1. Finite-State Basics</li>
# <li>2. Set Theory for Finite-State Networks</li>
# <li>3. Item & Process Morphology Using xfst Rules</li>
# <li>4. Example: English Adjectives</li>
# </ul>
#
# ## 1. Finite-State Basics
#
# ### 1.1. Finite-State networks
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
# <ul>
# <li>Inputs to the automaton are <i>symbols</i> like: <pre>m, e, c.</pre></li>
# <li>The set of valid symbols that the automaton will accept is its <i>alphabet</i>: <pre>{ a, c, e, g, i, m, n, o, r, s, t }</pre>.</li>
# <li>The sequences of symbols that the automaton will accept are <i>words</i> like: <pre>canto, mesa</pre>.</li>
# <li>The entire set of words that the automaton accepts or recognizes is its <i>language</i>: <pre>{ canto, mesa, tigre }</pre>.</li>
# </ul>
#
# ### 1.2. Sharing structure in minimal networks:
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
# <i>Images from Beesley & Karttunen (2003): Finite State Morphology.</i>
#
# ### 2.1. Examples of sets:
#
# <img src="img/two_sets.png">
#
# <img src="img/empty_set.png">
#
# ### 2.2. Some sets viewed as networks:
#
# <img src="img/empty_network.png">
#
# <img src="img/empty_string_network.png">
#
# ### 2.3. Some infinite sets:
#
# <img src="img/zero_or_more_a.png">
#
# <img src="img/universal_language.png">
#
# ### 2.4. Relations:
#
# <img src="img/lowercase2uppercase.png">
#
# The example above shows an infinite relation containing pairs, such as
# <code>{<"dog","DOG">,<"cat","CAT">,<"mouse","MOUSE">,...}</code>
#
# We can also have relations between lexical forms and surface forms, such as:
# <pre>
# {<"cantar+Verb+PresInd+1P+Sg", "canto">,
#  <"cantar+Verb+PresInd+1P+Pl","cantamos">,
#  <"canto+Noun+Masc+Sg","canto">, ...}
# </pre>
#
# ### 2.5. Union of sets
#
# <img src="img/union_of_sets.png">
#
# For instance, the union of the sets <code>{"clear", "clever", "ear", "ever"}</code> and <code>{"fat", "father"}</code> is
# <code>{"clear", "clever", "ear", "ever", "fat", "father"}</code>.

from hfst_dev import fst, disjunct
set1 = fst(('clear','clever','ear','ever'))
set2 = fst(('fat','father'))
union_set = disjunct((set1, set2))
print(union_set.extract_paths())

# The union shown as a network:
#
# <img src="img/union_of_sets_as_network.png">
#
# ### 2.6. Intersection of sets
#
# <img src="img/intersection_of_sets.png">
#
# For instance, the intersection of sets <code>{"clear", "clever", "ear"}</code> and <code>{"ear", "ever"}</code> is <code>{"ear"}</code>.

from hfst_dev import intersect
set1 = fst(('clear','clever','ear'))
set2 = fst(('ear','ever'))
intersection_set = intersect((set1, set2))
print(intersection_set.extract_paths())

# ### 2.7. Subtraction of one set from another
#
# <img src="img/subtraction_of_sets.png">
#
# For instance, the subtraction of sets <code>{"clear", "clever", "ear"}</code> and <code>{"clever", "ear"}</code> is <code>{"clear"}</code>.

from hfst_dev import subtract
set1 = fst(('clear','clever','ear'))
set2 = fst(('clever','ear'))
subtraction_set = subtract((set1, set2))
print(subtraction_set.extract_paths())

# ### 2.8. Concatenation of sets
#
# <img src="img/concatenation_of_sets.png">
#
# The concatenation is <code>{"works", "working", "worked"}</code>.

from hfst_dev import concatenate
set1 = fst(('work'))
set2 = fst(('s','ing','ed'))
concatenation_set = concatenate((set1, set2))
print(concatenation_set.extract_paths())

# ### 2.9. Composition of transducers
#
# <img src="img/composition.png">
#
# The composition is <code>{<"cat","Katze">}</code>.

from hfst_dev import compose
set1 = fst({'cat':'chat'})
set2 = fst({'chat':'Katze'})
composition_set = compose((set1, set2))
print(composition_set.extract_paths()) # TODO: @_EPSILON_SYMBOL_@ is printed

# ### 2.10. Projection
#
# <ul>
# <li>Projection is extracting one side of a relation.</li>
# <li>The upper/input projection of <code><"cat", "CHAT"></code> is "cat".</li>
# <li>The lower/output projection of <code><"cat", "CHAT"></code> is "CHAT".</li>
# </ul>
#
# <img src="img/projection.png">

cat = fst({'cat':'CHAT'})
cat.input_project()
cat.minimize() # get rid of epsilons
print(cat.extract_paths())

CHAT = fst({'cat':'CHAT'})
CHAT.output_project()
CHAT.minimize() # get rid of epsilons
print(CHAT.extract_paths())


# ### 2.11. Set operations expressed in the xfst language
#
# <pre>
# [ A | B ] denotes the union of the two languages or relations A and B ("or"-operation).
# [ A & B ] denotes the intersection ("and"-operation).
# [ A - B ] denotes the subtraction of B from A.
# [ A B ] denotes the concatenation.
# [ A .o. B ] denotes the composition of the relations.
# A.u denotes the upper (i.e. input) projection.
# A.l denotes the lower (o.e. output) projection.
# </pre>

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
# ### 3.1. Cascade of transducers: Rule 1
#
# Insert 'e' after the end of the stem in front of 's', if the stem ends in
# 's', 'x', 'ch', 'sh' or 'y'.
#
# Expressed as an xfst rule:
#
# <code>define InsertE   [. .] -> e || [ s | x | c h | s h | y ] %^ _ s ;</code>
#
# <img src="img/InsertE.png">

from hfst_dev import regex, HfstTransducer

InsertE = regex("[. .] -> e || [ s | x | c h | s h | y ] %^ _ s")
print(InsertE.lookup("sky^s'"))

# ### 3.2. Cascade of transducers: Rule 2
#
# Rewrite 'y' as 'i' when followed by the end of the stem, which is
# further followed by 'e'.
#
# Expressed as an xfst rule:
#
# <code>define YToI    y -> i || _ %^ e ;</code>
#
# <img src="img/YToI.png">

YToI = regex("y -> i || _ %^ e")
print(YToI.lookup("sky^es'"))

# ### 3.3. Cascade of transducers: Rule 3
#
# Remove the end of stem marker
#
# Expressed as an xfst rule:
#
# <code>define CleanUp    %^ -> 0 ;</code>

CleanUp = regex("%^ -> 0")
print(CleanUp.lookup("ski^es'"))

# <img src="img/CleanUp.png">
#
# ### 3.4. Cascade equivalent to single FST
#
# <img src="img/cascade.png">
#
# <i>Image from Beesley & Karttunen (2003): Finite State Morphology.</i>

from hfst_dev import compile_lexc_file
lexicon = compile_lexc_file('en_ia_morphology.lexc')

from hfst_dev import compose
cascade = compose((lexicon, InsertE, YToI, CleanUp))

# When our lexicon is composed with our rules, we can actually produce one
# single FST and 'jump' from the lexical-form input straight to the final
# output in one go, without producing the intermediate steps.
#
# <pre>
# Example input:  sky+N+Pl+Poss
# Lexicon output: sky^s'
# Rule 1 output:  sky^es
# Rule 2 output:  ski^es
# Rule 3 output:  skies
# </pre>
#
# The single FST will give directly: sky+N+Pl+Poss 🡒 skies.

print(cascade.lookup("sky+N+Pl+Poss"))

# ### 3.5. The order of the rules matters!
#
# What would happen if we reordered the rules (below) used in our simple
# English noun morphology?

cascade = compose((lexicon,YToI, InsertE, CleanUp))
print(cascade.lookup("sky+N+Pl+Poss"))

# ### 3.6. xfst notation explained in context
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
# <i>Images from Beesley & Karttunen (2003): Finite State Morphology.</i>

# ## 4. Example: English adjectives
#
# ### 4.1. Lexicon (lexc) of some English adjectives
#
# The file `en_ip_adjectives_lexicon.lexc`
#
# <pre>
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
# </pre>
#
# ### 4.2. Suggested xfst script for English adjectives
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
# <pre>
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
# </pre>
#
# ### 4.3. Corrected xfst script for English adjectives
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
# <pre>
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
# </pre>
#
# ## More information
#
# <ul>
# <li>Chapter 1 of the Beesley & Karttunen book: "A Gentle Introduction"</li>
# <li>Chapter 3 of the Beesley & Karttunen book: "The xfst Interface"</li>
# </ul>
