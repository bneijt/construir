#!/bin/bash
cd "`dirname "$0"`"
set -e -x
HP_VERSION=2012.4.0.0

mkdir -p job/bin
if [ ! -f "job/haskell-platform-${HP_VERSION}.tar.gz" ]; then
    wget "http://lambda.haskell.org/platform/download/${HP_VERSION}/haskell-platform-${HP_VERSION}.tar.gz" -O job/haskell-platform-${HP_VERSION}.tar.gz
fi
#Try to copy form ../opts
GHC_OPT_ARCHIVE="opt_ghc-7.4.2.tar.bz2"
if [ -f "../opts/${GHC_OPT_ARCHIVE}" ]; then
    cp "../opts/${GHC_OPT_ARCHIVE}" job
fi
if [ ! -f "job/${GHC_OPT_ARCHIVE}" ]; then
    echo "This job requires the job/${GHC_OPT_ARCHIVE}"
    echo "  which is the output from the ghc job"
    exit 1
fi

sed -s 's/HP_VERSION/'${HP_VERSION}'/g' < construir.template > job/bin/construir
sed -i 's/GHC_OPT_ARCHIVE/'${GHC_OPT_ARCHIVE}'/g' job/bin/construir
chmod a+x job/bin/construir

mkdir -p job/output
../mkjob.py --extra-space 1000 job

