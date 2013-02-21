Construir: _everybody can join_
===============================
The mean goal of construir is to set up a secure way to allow a build system to build jobs submitted by other people or a centralized server.


Status
=======
There is a basic image with a completely new approach and currently the jobs have to be recreated to conform to the new standard.

Drop the file in the queue directory, and the jobrunner will pick it up. When it's done, it will rename the image identification from "i100" to "d100" to mark the job as done.

Jobs are not allowed to take more then 3 hours.


First release is still to be made, nothing has a version number yet.

How it works
============
When a file is added to the queue directory, `jobrunner.py` will pick it up and start kvm with `image/i0.qcow2` as the first disk and the job as the second disk.

There is no network access for the job and after it is done, the machine will shutdown and the job will be moved to the done directory.

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
