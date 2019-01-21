Create notebooks from python files:

  jupytext --to notebook foo.py  # creates foo.ipynb

Create html files from notebooks:

  jupyter-nbconvert --to html foo.ipynb  # creates foo.html

Create images from att files
(works with HFST command line tools from branch hfst-dev-4.0):

  cat image11.att | hfst-txt2fst --named-states=Root --states-file=image11.states > image11.hfst
  cat image11.hfst | hfst-fst2txt --state-names=image11.states --format=dot > image11.dot
  dot -Tpng image11.dot -o image11.png

Create all ipynb and html files from py files:

  for file in */src/Part1.py; do echo $file && jupytext --to notebook $file ; done
  for file in */src/Part1.ipynb; do echo $file && jupyter-nbconvert --to html $file ; done
  for dir in */src/; do cd $dir && pwd && mv Part1.ipynb ../ && mv Part1.html ../ && cd ../.. ; done
