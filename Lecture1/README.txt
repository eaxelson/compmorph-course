Create notebooks from python files:

  jupytext --to notebook foo.py  # creates foo.ipynb

Create images from att files
(works with HFST command line tools from branch hfst-dev-4.0):

  cat image11.att | hfst-txt2fst --named-states=Root --states-file=image11.states > image11.hfst
  cat image11.hfst | hfst-fst2txt --state-names=image11.states --format=dot > image11.dot
  dot -Tpng image11.dot -o image11.png
  # display image11.png
