#!/bin/sh
exec qemu-system-x86_64 \
     -m 64M \
     -nographic \
     -kernel vm/bzImage \
     -append "console=ttyS0 loglevel=3 oops=panic panic=-1" \
     -no-reboot \
     -cpu qemu64 \
     -monitor /dev/null \
     -initrd vm/rootfs.cpio
