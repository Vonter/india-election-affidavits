#!/bin/bash

for ut in {01..09};
do
  mkdir -p "raw/U${ut}"

  if ! [ -f "raw/U${ut}/index.html" ]; then
    curl "https://affidavit.eci.gov.in/allConstList/U${ut}/24/PC/46%20/GENERAL" -o "raw/U${ut}/index.html"
    sleep 3
  fi

  constituencies=$(/usr/bin/grep -oP '"\K[^"\047]+(?=["\047])' raw/U$ut/index.html | grep -v "option" | grep -v "selected" | grep -v "value=")
  for constituency in $constituencies;
  do
    mkdir -p "raw/U${ut}/${constituency}"
    page=1
    candidates=10

    while [[ $candidates == 10 ]]
    do
      if ! [ -f "raw/U${ut}/${constituency}/${page}.html" ]; then
        curl "https://affidavit.eci.gov.in/CandidateCustomFilter?electionType=24-PC-GENERAL-1-46&election=24-PC-GENERAL-1-46&states=U${ut}&constId=${constituency}&submitName=100&page=${page}" -o "raw/U${ut}/${constituency}/${page}.html"
        sleep 3
      fi

      candidates=$(grep 'Constituency ' "raw/U${ut}/${constituency}/${page}.html" | wc -l)
      page=$((page+1))
    done
  done
done
