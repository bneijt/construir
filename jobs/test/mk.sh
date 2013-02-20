#!/bin/bash
tar -v -cJf test.tar.xz opt
truncate -s 1M test.tar.xz
