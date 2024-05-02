#!/bin/bash

for state in {01..29};
do
  mkdir -p "raw/${state}"

  if ! [ -f "raw/${state}/index.html" ]; then
    curl "https://affidavit.eci.gov.in/allConstList/S${state}/24/PC/46%20/GENERAL" -o "raw/${state}/index.html"
    sleep 3
  fi

  constituencies=$(/usr/bin/grep -oP '"\K[^"\047]+(?=["\047])' raw/$state/index.html | grep -v "option" | grep -v "selected" | grep -v "value=")
  for constituency in $constituencies;
  do
    mkdir -p "raw/${state}/${constituency}"
    page=1
    candidates=10

    while [[ $candidates == 10 ]]
    do
      if ! [ -f "raw/${state}/${constituency}/${page}.html" ]; then
        curl "https://affidavit.eci.gov.in/CandidateCustomFilter?electionType=24-PC-GENERAL-1-46&election=24-PC-GENERAL-1-46&states=S${state}&constId=${constituency}&submitName=100&page=${page}" -o "raw/${state}/${constituency}/${page}.html"
        sleep 3
      fi

      candidates=$(grep 'Constituency ' "raw/${state}/${constituency}/${page}.html" | wc -l)
      page=$((page+1))
    done
  done
done
