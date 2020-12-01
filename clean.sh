#! /bin/sh
filename=~/.visidata/plugins/pojobuddy.py
if [ -f "$filename" ]; then
    rm "$filename"
    echo "Deleted pojobuddy.py from ~/.visidata/plugins"
else
    echo "No plugins found to clean in ~/.visidata/plugins"
fi
