#!/bin/bash

for profile in $(/usr/bin/grep -Ri "show-profile" . | grep -v "div class" | cut -d '"' -f 2);
do
  id=$(echo $profile | cut -d '/' -f 9)

  if ! [ -f "raw/profiles/${id}" ]; then
    wget -d --header="User-Agent: curl/8.7.1" $profile -P "raw/profiles/"
    sleep 3
  fi
done
