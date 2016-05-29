#!/bin/bash
# -*- sh -*-

Here=$1
root=$2
url=$3
file=$4

title=$( awk 'gsub(/^#[ \t]*/,"") { print ; exit }' $file )

(cat $Here/etc/header.html
 cat $file | markdown_py                    \
  -x tables -x footnotes                     \
  -x def_list  -x toc -x smart_strong         \
  -x attr_list -x sane_lists  -x  fenced_code  \
  -x "codehilite(linenums=True)"
 cat $Here/etc/footer.html
)                          |
python $Here/etc/xpand.py |
sed -e "s/\$FiLe/$file/g"     \
    -e "s/\$TiTlE/$title/g"    \
    -e "s?\$IcOnS?/img/icons?g" \
    -e "s?\$ImG?/img?g"          \
    -e "s?\$RoOt?$root?g"         \
    -e "s?\$UrL?$url?g"
