#!/bin/bash

TOKEN=$1
RECIPIENTS_ID=(`echo $2 | sed 's/,/\n/g'`)
API_URL="https://api.telegram.org"
TEXT=`cat`
if [[ -z $TOKEN ]] || [[ -z $2 ]] ; then
  echo "Usage: ./bash_telegram_notify.sh botTELEGRAM_BOT_TOKEN userid1,userid2,userid3"
  echo "Example: ./bash_telegram_notify.sh bot1232145125:AAAAAAAAA_BBBBBBB 13213123,23123213,213213"
  exit 1
fi

function send_message(){
  curl -s -X POST \
  -Ftext=`cat` -Fchat_id=$1 -Fparse_mode="Markdown"\
  "$API_URL/$TOKEN/sendMessage"
}

for RECIPIENT in "${RECIPIENTS_ID[@]}"
do
  echo $TEXT | send_message $RECIPIENT
done
