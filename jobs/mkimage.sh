#!/bin/bash
JOBDIR="$1"
if [ ! -d "$JOBDIR" ]; then
    echo "First argument must be a directory"
    exit 1
fi

set -e
if [ ! -f job.img ]; then
    dd if=/dev/zero of=job.img bs=1024 count=2M
fi
mkfs.ext4 -F -O ^has_journal job.img
sudo mount -o loop job.img tmp
cp -r "$JOBDIR"/* tmp
sleep 1
sudo umount tmp


