Construir: _everybody can join_
===============================
The mean goal of construir is to set up a secure way to allow a build system to build jobs submitted by other people or a centralized server.


Roadmap
=======
Done

 - Build image created
 - Test job created and a script to package up a git repo as a job

Currently being done

 - Create a more or less feature complete image, to do most of the build heavy lifting

**Future:** The future is to create a website that will host jobs and results. The jobrunner will then be transformed into a job that download, executes and then uploads a job, making it possible for people to run such a jobrunner at home or on their spare server.


How it works
============
When a file is added to the queue directory, `jobrunner.py` will pick it up and start kvm with `image/i0.qcow2` as the first disk and the job as the second disk.

There is **no network access for the job** and after it is done, the machine will shutdown and the job will be moved to the done directory.

A job can output by using the space of the device, this means a job must know it's output size before hand.


Execute `./jobrunner.py`, then add a job image to the `queue` directory to see it working.


Build images
============
There can be multiple version of a build system to kick of a job, each has it's own number which is listed in [image README on the git repository](https://github.com/bneijt/construir/tree/master/image).

Creating a job
==============
You can look at the example jobs in the jobs directory of this repository, but the basic idea is very simple:

1. Create a bash script under the name `job/construir` and add the following code to it:

        date > /tmp/test.txt
        tar -cJf /dev/sdb /tmp/test.txt

2. Package that script into an XZ compressed tar archive, put i0 in the filename to make it run on the image with index 0:

        tar -cJf testjob_i0.tar.xz opt

3. Increase the size of the job to make sure it can contain all the extra output:

        truncate +1M testjob_i0.tar.xz

That's it. Now put the job in a queue directory of a `jobrunner.py`.

Creating a build image
======================
See the [build image readme](tree/master/image).

Caveats
=======

 * A job may not be smaller then approximately 500K.

