# Kenneth R. Beesley and Lauri Karttunen: Finite State Morphology,
# CSLI Publications, 2003
# (http://press.uchicago.edu/ucp/books/book/distributed/F/bo3613750.html)
#
# Daniel Jurafsky and James H. Martin, Speech and Language Processing,
# Prentice Hall, second edition, 2009
#
#
# | Week 1 | (Introduction), lexc, xfst, replace rules |
# | Week 2 | Weighted finite state machines, (unsupervised morphology) |
# | Week 3 | Regular expressions, pronunciation lexicons, guessers, stemmers, twolc, two-level rules |
# | Week 4 | Flag diacritics, non-concatenative morphology |
# | Week 5 | Optimization of finite-state networks |
# | Week 6 | (Guest lecture) |
# | Week 7 | (Final project demos, technical presentetions) |
#
#
# ## Hockett's models of morphology
#
# ### Word and Paradigm (W&P), Example: Finnish nouns
#
# | Cases/Numbers | Singular | Plural |
# | Nominative | susi | sudet | 
# | Genitive | suden | susien, sutten |
# | Partitive | sutta | susia |
# | Inessive | sudessa | susissa |
# | Elative | sudesta | susista |
# | Illative | suteen | susiin |
# | Adessive | sudella | susilla |
# | Ablative | sudelta | susilta |
# | Allative | sudelle | susille |
# | Essive | sutena | susina |
# | Translative | sudeksi | susiksi |
# | Instructive | - | susin |
# | Abessive | sudetta | susitta |
# | Comitative | - | susine(en) |
#
# ### Item and Arrangement (I&A)
#
# * Morphemes and allomorphs
#  - "SUSI": susi, sude-, sute-, sut-, sus-
#  - Number:
#    * Singular: Ö (or no morpheme at all: unmarked)
#    * Plural: -t, -i-, -j-
#  - Case:
#    * Genitive: -n, -en, -den, -tten
#    * Partitive: -a, -ä, -ta, -tä
#    * Etc.
# * The allomorphs occur in a specific distribution:
#  - E.g., sus- in all plural forms except nominative
#  - No allomorph is more "basic" than any other.
#
# ## Item and Process (I&P)
#
# We have roots or bases of morphemes and different processes apply to them:
# - "SUTE"
# - Nominative: word final 'e' becomes 'i'; 't' in front of 'i' becomes 's' => "susi"
# - Genitive: add suffix '+n'; soften 't' to 'd' in closed syllable => "suden"
# - Etc.

