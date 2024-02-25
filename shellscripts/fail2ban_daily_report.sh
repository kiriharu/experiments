#!/bin/bash

YESTERDAY_DATE=`date --date="yesterday" +%Y-%m-%d`

function findByAction {
    echo `zgrep -E "$1 [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" /var/log/fail2ban.log* | grep $YESTERDAY_DATE | awk '{print $6}' | sed 's/[][]//g' | sort | uniq -c | awk '{print $2, $1}'`
}

BANS=`findByAction "Ban"`
UNBAN=`findByAction "Unban"`
FOUND=`findByAction "Found"`

MESSAGE="📕 Fail2Ban report ($YESTERDAY_DATE)

⭐️ Banned by services:
$BANS
⭐️ Unbanned by services:
$UNBAN
⭐️ Found by services:
$FOUND

🖥 Hostname: $HOSTNAME"

echo "$MESSAGE"
