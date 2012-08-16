#!/bin/bash
/etc/init.d/mountall.sh
cd /job
PATH="/job/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" ./run.sh
/sbin/poweroff
