awk -F',' '{if($6=="\"Total\"" && $7 == "\"Total\""){print $2","$3","$5","$8} }' D02.csv > D02-simple.csv
grep -v ",\"00\"" D02-simple.csv | grep -v "^\"07\"" > temp
grep  "^\"07\",\"00" D02-simple.csv >> temp
sort temp| sed s/" "/_/g | sed s/\"//g | sed s/Uttranchal/Uttaranchal/g | sed s/gargh/garh/g | sed s/Chhatis/Chhattis/g | sed s/"&"/and/g | sed s/A_and_N_Islands/Andaman_and_Nicobar/g > cleanedUp_migration_data.csv
