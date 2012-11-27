#!/bin/bash
IMAGE="$1"
if [ ! -f "$IMAGE" ]; then
    echo "First argument should be an image file"
    exit 1
fi

set -e
MOUNTPOINT="/tmp/e2_extract_$$"
mkdir "$MOUNTPOINT"
fuse-ext2 "$IMAGE" "$MOUNTPOINT"
if [ -d "$MOUNTPOINT"/"output" ]; then
    cp -r "$MOUNTPOINT"/"output" "$IMAGE"_output
else
    echo "$IMAGE does not contain an output directory"
fi
fusermount -u "$MOUNTPOINT"
rmdir "$MOUNTPOINT"

