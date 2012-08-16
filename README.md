Open build system
=================

    Any computer should be able to open up it's doors to build jobs for the open source community.


How it works
============
A debian system is booted with a root filesystem in snapshot mode and a job image (filesystem image) in writable mode. The job can then create, delete and add files anywhere with root privileges. After the job is done, the system is automatically shut down.

A simple job tracker will move job images from a queue folder, uncompress them, boot the machine with the job image, kill the machine if it takes more then two hours to complete and finally place the compressed job image in the done folder.


Current image
=============
The current worker image has debian image with Vagrant like credentials:
- Root password: vagrant

TODO
- Real job control, with a wait on the pid and a timeout instead of a polling loop.
- Create a script to package a directory into a FS image.

- IO event based polling of queue, only pick up a job when a file is closed to make sure upload is completed.
- Create a job configuration which contains dependencies to allow for jobs to have precompiled stuff included.
- Configure an FTP server to allow for job uploads
- Add security by checking the uploaded job filetype (just with file)
- Clean up the done directory periodically


FS todo: disable journal, add runjob script to system etc. Add mount raw image to git repo

Creating a base image by hand
=============================
To create the base image, I did the following:

 - Use the debian netinst image in expert install mode to create a minimal debian installation
 - Remove unneeded packages where appropriate
 - Mount the disk image separately (using the `rawmount.sh` script running it as root)
 - Copy the files to their right location:
    - `40_custom` to `/etc/grub.d/` to add the Job boot option to grub
    - grub to `/etc/default/` to make Job the default job selected and boot time to 2 seconds
    - `runjob.sh` to `/root/` to start the job and poweroff the machine afterwords
 - Boot the image and run `update-grub` to activate the new grub configuration.
 
There is currently no script for this process, however you can download a pre-made debian image from the download section.

Creating a job image by hand
============================
Creating job images is simple. Job images are single files with a readable filesystem (for example `ext2`).

 - Create an empty file `dd if=/dev/zero of=job.img bs=1M count=10`, where count is the number of megabytes.
 - Format the empty file: `mkfs.ext2 job.img`
 - Mount the image and add your files files to it. Use `mkdir jobdir` then `sudo mount -o loop job.img jobdir` and add your job files.

After creating the iamge, compress it and you should be able to use it for any Construir server.




