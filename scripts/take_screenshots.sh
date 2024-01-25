#!/bin/bash

# set the internal field separator to a newline character to handle spaces in filenames correctly
IFS=$'\n'
# get the current directory
CURRENT_DIR=$(pwd)

for folder in "$1"; do
  if [ -d "$folder" ]; then
    category=$(basename "$folder")
    echo "Processing category: $category"
    total_folders=0

    for file in "$folder"/*.vrm; do
      if [ -f "$file" ]; then
        vrm_filename=$(basename "$file")
        png_file="$folder/$(basename "$vrm_filename" .vrm).png"
        if [ ! -f "$png_file" ] || [ "$file" -nt "$png_file" ]; then
          if node ./node_modules/.bin/screenshot-glb -i "$file" -w 512 -h 512 -m "orientation=0 0 120" -o "$png_file"; then
            echo "Screenshot of $vrm_filename saved as $(basename "$vrm_filename" .vrm).png"
          else
            echo "Failed to take a screenshot of $vrm_filename"
          fi
        fi
      fi
    done
  fi
done

# Reset the internal field separator to the default value
unset IFS
