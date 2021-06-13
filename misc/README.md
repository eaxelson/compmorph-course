# compmorph-course

Jupyter notebook files for course Computational Morphology with HFST.

This web course is based largely on the course ”Computational Morphology” (https://courses.helsinki.fi/en/LDA-T3101/120259674) held at the University of Helsinki spring 2018.
The course was taught and planned by Mathias Creutz. Senka Drobac also contributed to the exercises.
The web course uses the same examples and exercises, but HFST command line tools have been replaced with HFST Python interface.


## Blueprint configuration

name:
"Computational Morphology with HFST (test version)"

description:
"Environment for self-study course Computational Morphology with HFST.
 The course demonstrates how HFST tools can be used for generating finite-state morphologies."

environment variables for docker, separated by space:
"AUTODOWNLOAD_URL=https://raw.githubusercontent.com/eaxelson/compmorph-course/master/src/bootstrap.bash
 AUTODOWNLOAD_EXEC=bootstrap.bash"
