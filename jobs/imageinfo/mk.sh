#!/bin/bash
tar -cJf imageinfo_i0.tar.xz job
truncate -s +1M imageinfo_i0.tar.xz
