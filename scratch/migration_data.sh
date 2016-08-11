awk -F',' '{if($6=="\"Total\"" && $7 == "\"Total\""){print $2","$3","$5","$8} }' D02.csv > D02-simple.csv
grep -v "00" D02-simple.csv | grep -v "^\"07\"" > temp
grep  "^\"07\",\"00" D02-simple.csv >> temp
sort temp| sed s/" "/_/g | sed s/\"//g  > cleanedUp_migration_data.csv
