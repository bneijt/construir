Construir: _everybody can join_
===============================
The mean goal of construir is to set up a secure way to allow a build system to build jobs submitted by other people or a centralized server.


Status
=======
After working with the creation of ext images using userspace tools, I've decided to drop full disk images and go with tar.xz files.

The new approach is as follows:
- Tar your files into an archive using tar -cJf archive.tar.xz yourfiles
- Truncate the tar file to the size you require it to be for your output: truncate --size 10m archive.tar.xz
- Rename the file to contain the image you want it to run on and something to identify it: jobname_i100.tar.xz

Drop the file in the queue directory, and the jobrunner will pick it up. When it's done, it will rename the image identification from "i100" to "d100" to mark the job as done.

Jobs are not allowed to take more then 3 hours.



First release is still to be made, nothing has a version number yet.

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
 - Install build-essential and bzip2
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
Create a directory with a bash script under the path `bin/construir` and package it up into an ext2 filesystem image. Use the `jobs/mkjob.py` script with the directory as an argument, which will create an ext2 image with the same name as the directory.


