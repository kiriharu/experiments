#!/bin/bash

API_URL="https://api.telegram.org"
while getopts "t:u:" opt
do
case $opt in
  t)TOKEN=$OPTARG
    ;;
  u)RECIPIENTS_ID=(`echo $OPTARG | sed 's/,/\n/g'`)
    ;;
esac
done

shift $((OPTIND - 1))
TEXT=$1

if [[ -z $TOKEN ]] || [[ -z $RECIPIENTS_ID ]] ; then
  echo "Usage: ./bash_telegram_notify.sh -t botTELEGRAM_BOT_TOKEN -u userid1,userid2,userid3 message "
  echo "Example: ./bash_telegram_notify.sh -t bot1232145125:AAAAAAAAA_BBBBBBB -u 13213123,23123213,213213 hellow!!!"
  exit 1
fi

function send_message(){
  curl -s -X POST -Ftext=\<-  -Fchat_id=$1 \
  -Fparse_mode="html" \
  "$API_URL/$TOKEN/sendMessage"
}

for RECIPIENT in "${RECIPIENTS_ID[@]}"
do
  echo "$TEXT" | send_message $RECIPIENT
done
