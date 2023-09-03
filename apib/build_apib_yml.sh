#!/bin/bash
# read all API blueprint files and create YML files for each
rm ~/Documents/workspace/wxc_sdk/private/apib/apib_yml/*.yml || true
find ~/Documents/workspace/api-specs/blueprint/webexapis.com/v1 -iname "*.apib" -print0 | while read -d $'\0' file
do
  bn=$(basename "$file")
  yml="${bn%.apib}.yml"
  # echo "$file" "$bn" "$yml"
  drafter -f json "$file" -o ~/Documents/workspace/wxc_sdk/private/apib/apib_yml/$yml
done
