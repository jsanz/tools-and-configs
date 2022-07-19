#!/bin/sh

if [ -f /tmp/dunst-paused ]; then
    echo "🔇"
else
    echo "🗣️"
fi
