Open build system
=================

    Any computer should be able to open up it's doors to build jobs for the open source community.


How it works
============
A debian system is booted and the job image is mounted and run. It will run for a maximum of two hours and then shutdown.

The result of the job (the same job image) is moved to the done folder.

- Root password: vagrant
- User: vagrant
- Password: vagrant

TODO
- Real job control, with a wait on the pid and a timeout instead of a polling loop.
- Create a script to package a directory into a FS image.

- IO event based polling of queue, only pick up a job when a file is closed to make sure upload is completed.
- Create a job configuration which contains dependencies to allow for jobs to have precompiled stuff included.
- Configure an FTP server to allow for job uploads
- Add security by checking the uploaded job filetype (just with file)
- Clean up the done directory periodically

