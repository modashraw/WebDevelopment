#!/bin/bash
ssh 192.168.245.24 'sync; echo 3 > /proc/sys/vm/drop_caches';
ssh 192.168.245.27 'sync; echo 3 > /proc/sys/vm/drop_caches';
ssh 192.168.245.37 'sync; echo 3 > /proc/sys/vm/drop_caches';
sync; echo 3 > /proc/sys/vm/drop_caches