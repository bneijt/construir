Open build system
=================

    Any computer should be able to open up it's doors to build jobs for the open source community.


How it works
============
A debian system is booted with a root filesystem in snapshot mode and a job image (filesystem image) in writable mode. The job can then create, delete and add files anywhere with root privileges. After the job is done, the system is automatically shut down.

A simple job tracker will move job images from a queue folder, uncompress them, boot the machine with the job image, kill the machine if it takes more then two hours to complete and finally place the compressed job image in the done folder.

Extracting the information from the job and automatically creating jobs for certain situations is the second phase of the project.

Current image
=============
The current worker image has debian image with Vagrant like credentials:
- Root password: vagrant

Roadmap
=======
- Create a real job controlling system, not a simple script that polls, among it's tasks will be
    - Remove queue and done jobs older then X amount of time
    - Start and kill the server without polling
    - Wait for a file to be uploaded and closed again before running the job (using inotify features of the kernel)
- Create example jobs and have a management script that can automatically package a job and extract the result.
- Add a method of including precompiled or earlier compiled jobs using some kind of dependency tracking or long lived job outputs?

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




