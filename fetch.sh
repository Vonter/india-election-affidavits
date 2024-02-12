#!/bin/bash

for year in 2009 2014;
do
  mkdir -p "raw/Lok Sabha/${year}"
  for id in {1..600};
  do
    curl "https://myneta.info/ls${year}/index.php?action=show_candidates&constituency_id=${id}" > "raw/Lok Sabha/${year}/${id}.html"
    sleep 5
  done
done

for year in 2004;
do
  mkdir -p "raw/Lok Sabha/${year}"
  for id in {1..600};
  do
    curl "https://myneta.info/loksabha${year}/index.php?action=show_candidates&constituency_id=${id}" > "raw/Lok Sabha/${year}/${id}.html"
    sleep 5
  done
done

for year in 2019;
do
  mkdir -p "raw/Lok Sabha/${year}"
  for id in {1..1200};
  do
    curl "https://myneta.info/LokSabha${year}/index.php?action=show_candidates&constituency_id=${id}" > "raw/Lok Sabha/${year}/${id}.html"
    sleep 5
  done
done

rm $(/usr/bin/grep "Page Not Found" -l -R . | grep -v "fetch.sh")
