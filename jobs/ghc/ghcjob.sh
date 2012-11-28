#!/bin/bash
cd "`dirname "$0"`"
set -e -x
GHC_VERSION=7.4.2

mkdir -p job/bin
if [ ! -f "job/ghc-${GHC_VERSION}.tar.bz2" ]; then
    wget "http://www.haskell.org/ghc/dist/${GHC_VERSION}/ghc-${GHC_VERSION}-x86_64-unknown-linux.tar.bz2" -O job/ghc-${GHC_VERSION}.tar.bz2
fi

sed -s 's/GHC_VERSION/'${GHC_VERSION}'/g' < construir.template > job/bin/construir
chmod a+x job/bin/construir

mkdir -p job/output
../mkjob.py --extra-space 1000 job

