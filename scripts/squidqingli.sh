#!/bin/sh
squidcache_path="/usr/local/squid/var/cache"
squidclient_path="/usr/local/squid/bin/squidclient"
#grep -a -r $1 $squidcache_path/* | grep "http:" | awk -F 'http:' '{print "http:"$2;}' | awk -F\' '{print $1}' > cache.txt
if [[ "$1" == "swf" || "$1" == "png" || "$1" == "jpg" || "$1" == "ico" || "$1" == "gif" || "$1" == "css" || "$1" == "js" || "$1" == "html" || "$1" == "shtml" || "$1" == "htm"   ]]; then
grep -a -r .$1 $squidcache_path/* | strings | grep "http:" | awk -F 'http:' '{print "http:"$2;}' | awk -F\' '{print $1}' | grep "$1$" | uniq > cache.txt
else
grep -a -r $1 $squidcache_path/* | strings | grep "http:" | awk -F 'http:' '{print "http:"$2;}' | awk -F\' '{print $1}' | uniq > cache.txt
fi
cat cache.txt | while read LINE
do
$squidclient_path -p 80 -m PURGE $LINE
done
