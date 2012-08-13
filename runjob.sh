#!/bin/bash

if [[ ! -d "queue" ]]; then mkdir "queue"; fi
if [[ ! -d "done" ]]; then mkdir "done"; fi


for f in queue/*; do
    START="`date +"%F-%H.%M"`"
    mv "$f" job.img
    kvm -net none -no-fd-bootchk -nographic -enable-kvm -no-reboot -drive file=debian.img,index=0,media=disk,snapshot=on -drive file=job.img,index=1,media=disk &
    KVM_PID="$!"
    echo "KVM pid is $KVM_PID"
    #Sleep a maximum of 120 minutes
    for minute in {1..120}; do 
        if [[ ! -d "/proc/$KVM_PID" ]]; then
            break
        fi
        sleep 1m
    done
    if [[ -d "/proc/$KVM_PID" ]]; then
        kill -9 "$KVM_PID"
    fi
    mv job.img done/"${START}_`basename "$f"`" 
done


