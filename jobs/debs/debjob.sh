#!/bin/bash
cd "`dirname "$0"`"
set -e -x

chmod a+x job/bin/construir
mkdir -p job/output
../mkjob.py --extra-space 50 job
