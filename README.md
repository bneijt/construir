Open build system
=================

    Any computer should be able to open up it's doors to build jobs for the open source community.

Status
=======
The `jobrunner.py` script will run job files form the queue directory. Creating jobs needs to still be easier.

TODO: jobrunner needs polish and configuration options.

How it works
============
A Debian system is booted with a root file system in snapshot mode and a job image (file system image) in writable mode. The job can then create, delete and add files anywhere with root privileges. After the job is done, the system is automatically shut down.

A simple job tracker will move job images from a queue folder, boot the machine with the job image, kill the machine if it takes more then two hours to complete and finally place the resulting job image in the done folder in `xz` compressed form.

Execute `./jobrunner.py`, then add a job image to the `queue` directory to see it working.


Current image
=============
You can download a basic debian image with the software installed from github. The password for the root user is `root`.




Creating a base image by hand
=============================
To create the base image, I did the following:

 - Use the Debian `netinst` image in expert install mode to create a minimal Debian installation
 - Remove unneeded packages where appropriate
 - Mount the disk image separately (using the `rawmount.sh` script running it as root)
 - Copy all the files from the `config` directory onto the filesystem.
 - Boot the system and run `update-rc.d construir defaults`

The `/usr/sbin/construir` script will try to run a job script from `/job/bin/construir`,
create a `/job/zero` file and `poweroff`.
This means you will no longer be able to boot and log in without a job. 
To disable it, use the `rawmount.sh` script to mount and comment out
the `poweroff` in `/usr/sbin/construir`. 

There is currently no script for this process, however you can download a pre-made Debian image from the download section.

Creating a job image
====================
By hand
-------
Creating job images is simple. Job images are single files with a readable file system (for example `ext2`).

 - Create an empty file `dd if=/dev/zero of=job.img bs=1M count=10`, where count is the number of megabytes.
 - Format the empty file: `mkfs.ext2 job.img`
 - Mount the image and add your files files to it. Use `mkdir jobdir` then `sudo mount -o loop job.img jobdir` and add your job files.

Using `mkimage.sh`
------------------
The `mkimage.sh` script in the jobs directory takes a directory as an argument and performs the above steps for you. Because of having to mount the job image as root, you will be asked for your `sudo` password.

The resulting image will be called `job.img`


