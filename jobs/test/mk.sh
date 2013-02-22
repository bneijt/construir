#!/bin/bash
tar -v -cJf test_i0.tar.xz job
truncate -s +500K test_i0.tar.xz
