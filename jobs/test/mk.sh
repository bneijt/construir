#!/bin/bash
tar -v -cJf test.tar.xz job
truncate -s 1M test.tar.xz
