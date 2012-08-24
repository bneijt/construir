#!/bin/bash
#    This file is part of Construir.
#
#    Construir is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Construir is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Construir.  If not, see <http://www.gnu.org/licenses/>.
if [ "x$1" == "x" ]; then
  echo "Usage: rawmount device_dump.raw"
  exit 1
fi
if ! which kpartx >/dev/null 2>&1; then
    echo "Error: this script requires kpartx to work"
    exit 1
fi

image=$1
kpartx -a "$image" || exit
#OLD losetup -f "$image" || exit
mountPoint="/tmp/mount_$$/"
echo "Image      : $image"
echo "Mount base : $mountPoint"
#loDev=`losetup --associated "$image"| cut -d ":" -f 1|tail -n1`
#echo "Lo device  : $loDev"
#parts=`fdisk -l "$loDev" |awk -- '/^\/dev.*\*/{print $1}'`


parts=`kpartx -l "$image"|cut -d : -f 1|tr -d '\n'`
i=0
echo "Partitions : $parts"
for device in $parts; do
   echo "Mounting: ${device}"
   mp="${mountPoint}${i}"
   mkdir -p "${mp}"
   mount "/dev/mapper/$device" "${mountPoint}${i}" || rmdir "${mp}"
   let i=i+1
done
#Hide our failures
rmdir "${mountPoint}" 2>/dev/null >/dev/null

