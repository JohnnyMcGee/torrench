#! /bin/bash

# Convert a magnet URI into a .torrent file
# Run the script with:
# ./magnet2torrent.sh "MAGNET_URI"
# (Don't forget the quotes aroud MAGNET_URI)

cd /home/rahkshi/torrents || exit    # set your watch directory here
[[ "$1" =~ xt=urn:btih:([^&/]+) ]] || exit
hashh=${BASH_REMATCH[1]}
if [[ "$1" =~ dn=([^&/]+) ]];then
    filename=${BASH_REMATCH[1]}
else
    filename=$hashh
fi
echo "d10:magnet-uri${#1}:${1}e" > "meta-$filename.torrent"