#!/bin/bash
#set -x

CURRENT_VERSION=$1
LATEST_VERSION_URL="http://api.vintagestory.at/lateststable.txt"
APPRISE_API_HUB="https://enter.your.url/notify/token-here"

function get_latest_version {
   curl -X GET $LATEST_VERSION_URL
}


LATEST_VERSION=`get_latest_version`
if [ $CURRENT_VERSION != $LATEST_VERSION ] ; then
    MESSAGE="🎮 New VintageStory update available!
📌 Current version: $CURRENT_VERSION
📌 Latest version: $LATEST_VERSION"
    curl -X POST \
    -d "tags=all,vintagestory&body=$MESSAGE" \
    $APPRISE_API_HUB
fi
