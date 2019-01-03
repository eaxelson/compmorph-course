#!/bin/bash

cd /home/jovyan/

# rm -r work

export GIT_COMMITTER_NAME=anonymous
export GIT_COMMITTER_EMAIL=anon@localhost

git clone https://github.com/eaxelson/hfst-notebooks.git

python3 -m pip install hfst-dev
# python3 -c "import hfst_dev"
