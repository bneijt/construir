#!/bin/bash
JOBDIR="$1"
if [ ! -d "$JOBDIR" ]; then
    echo "First argument must be a directory"
    exit 1
fi

set -e
if [ ! -f job.img ]; then
    truncate -s 1G job.img
fi
mkfs.ext4 -F -O ^has_journal job.img
fuse-ext2 -o rw+ job.img tmp
cp -r "$JOBDIR"/* tmp
sleep 1
fusermount -u tmp


