#!/bin/bash
set -e
if [ ! -f "$1" ]; then
    echo "First argument must be a job image"
    exit 1
fi
EMULATOR="`which kvm`"
if [ -z "$EMULATOR" ]; then
    EMULATOR="`which qemu`"
fi
exec "$EMULATOR" -no-fd-bootchk -enable-kvm -no-reboot -drive file=debian.raw,index=0,media=disk,snapshot=on -drive file="$1",index=1,media=disk


