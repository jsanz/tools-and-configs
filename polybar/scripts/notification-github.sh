#!/bin/sh

USER="jsanz"
TOKEN="$(cat "${HOME}/.config/polybar/github")"

data=$(echo "user = \"$USER:$TOKEN\"" | curl -sf -K- "https://api.github.com/notifications") 

all_notifications=$(echo "${data}" | jq -r ". | length")

if [ "$all_notifications" -gt 0 ]; then
    echo "${all_notifications}"
else
    echo ""
fi
