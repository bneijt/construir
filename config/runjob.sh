#!/bin/bash
/etc/init.d/mountall.sh
/bin/rm -rf /job/zero
cd /job
PATH="/job/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" /bin/bash run.sh
/bin/dd if=/dev/zero of=/job/zero
/sbin/poweroff
