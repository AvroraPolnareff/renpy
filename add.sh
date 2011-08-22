#!/bin/sh

if [ "x$1" = "x" ]; then
    echo need version
    exit
fi

rsync -av updates tom@onegeek.org:/home/tom/WWW.update/renpy/

mkdir ~/ab/website/renpy/dl/$1
cp dists/renpy-$1-* ~/ab/website/renpy/dl/$1
cp renpy-ppc.zip ~/ab/website/renpy/dl/$1

cd ~/ab/website
./upload.sh
