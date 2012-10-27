Construir opens up a computer to sandboxed calculation jobs that last for a maximum of two hours and are not allowed to require any kind of internet access.

Jobs are submitted via FTP as disk images, run by a Qemu machine and then copied to the output directory. Output is available for 24 hours after completion.

Build
=====
 * Create a debian base installation
 * Copy all the files from the `config` directory onto the filesystem
 * Boot the system and run "update-rc.d construir defaults"

Construir will try to run the job from /job and poweroff afterwards, 
so you will nolonger be able to boot the image without a job.
To disable it, use the `rawmount.sh` script to mount and comment out
the `poweroff` in `/usr/sbin/construir`.






