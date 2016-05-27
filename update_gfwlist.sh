#!/bin/bash
# update_gfwlist.sh
# Author : VincentSit
# Copyright (c) http://xuexuefeng.com
#
# Example usage
#
# ./whatever-you-name-this.sh
#
# Task Scheduling (Optional)
#
#	crontab -e
#
# add:
# 30 9 * * * sh /path/whatever-you-name-this.sh
#
# Now it will update the PAC at 9:30 every day.
#
# Remember to chmod +x the script.


GFWLIST="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"
PROXY="127.0.0.1:1080"
GFWLIST_JS="gfwlist.js"
USER_RULE_NAME="user-rule.txt"
TMP_FILE_PATH=/tmp/gfwlist.txt
SSX_PATH=~/.ShadowsocksX/
MYPWD=$(pwd)

update_gfwlist()
{
	echo "Downloading gfwlist."

	curl -s "$GFWLIST" --fail --socks5-hostname "$PROXY" --output $TMP_FILE_PATH

	if [[ $? -ne 0 ]]; then
		echo "abort due to error occurred."
    exit 1
	fi

	cd $SSX_PATH || exit 1

	if [ -f $GFWLIST_JS ]; then
		mv $GFWLIST_JS ~/.Trash
	fi

	if [ ! -f $USER_RULE_NAME ]; then
		touch $USER_RULE_NAME
	fi

	cd $MYPWD
	python3 ./main.py \
    --input $TMP_FILE_PATH \
    --file $SSX_PATH$GFWLIST_JS \
    --proxy "SOCKS5 $PROXY; SOCKS $PROXY; DIRECT;" \
    --user-rule $SSX_PATH$USER_RULE_NAME \
    --precise

  rm -f $TMP_FILE_PATH

  echo "Updated."
}

update_gfwlist