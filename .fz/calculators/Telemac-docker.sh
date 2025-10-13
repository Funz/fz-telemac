#!/bin/bash

# if direcotry as input, cd into it
if [ -d "$1" ]; then
  cd "$1"
  CAS=`ls *.cas | head -n 1`
  shift
# if $* are files, find the .cas file
elif [ $# -gt 1 ]; then
  CAS=""
  for f in "$@"; do
    if [ `echo $f | grep -c '\.cas$'` -eq 1 ]; then
      CAS="$f"
      break
    fi
  done
  if [ -z "$CAS" ]; then
    echo "No .cas file found in input files. Exiting."
    exit 1
  fi
  shift $#
else
  echo "Usage: $0 <case.cas or case_directory>"
  exit 2
fi

if [ 1 -le `echo \`pwd -P\` | grep --color='auto' -P -n "[\x80-\xFF]" | wc -l` ]; then
  echo "Telemac will not support non ISO char in path. Exiting."; 
  exit 3
fi

NCPU=`grep ^cpu\\\\scores /proc/cpuinfo | uniq |  awk '{print $4}'`

docker run -v `echo $PWD`:/workdir irsn/telemac-mascaret:latest telemac2d.py --ncsize=$NCPU $CAS &

PID=$!
echo $PID >> PID
wait $PID
rm -f PID
