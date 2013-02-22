Makes a construir job from a git repo with a construir script in it.

This job contains a job script which will call the script form the git repo and afterwards collect all output from `repo/artifacts` to the result xz file.

Usage
=====

 1. Checkout clone the repo under the name `repo`

    git clone git://somewhere/something repo

 2. Stand next to the `mk.py` file and run `./mk.py`

Example repo/construir
======================
repo/construir just contains the tasks to build the image.

    ./configure && make && make install
