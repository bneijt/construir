#!/bin/bash
set -e

if [[ ! -d "queue" ]]; then mkdir "queue"; fi
if [[ ! -d "done" ]]; then mkdir "done"; fi

EMULATOR="`which kvm`"
if [ -z "$EMULATOR" ]; then
    EMULATOR="`which qemu`"
fi

for f in queue/*; do
    START="`date +"%F-%H.%M"`"
    mv "$f" job.img
    "$EMULATOR" -net none -no-fd-bootchk -nographic -enable-kvm -no-reboot -drive file=debian.raw,index=0,media=disk,snapshot=on -drive file=job.img,index=1,media=disk &
    KVM_PID="$!"
    echo "KVM pid is $KVM_PID"
    #Sleep a maximum of 120 minutes
    for minute in {1..120}; do 
        sleep 1m
        if [[ ! -d "/proc/$KVM_PID" ]]; then
            break
        fi
    done
    if [[ -d "/proc/$KVM_PID" ]]; then
        kill -9 "$KVM_PID"
    fi
    xz -0 job.img
    mv job.img.xz done/"${START}_`basename "$f"`".xz
done


