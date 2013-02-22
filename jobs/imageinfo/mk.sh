#!/bin/bash
tar -cJf imageinfo_i0.tar.xz job
truncate -s +500K imageinfo_i0.tar.xz
