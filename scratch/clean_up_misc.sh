python -m json.tool ../resources/in-2001.json| grep "\"id\"\|state" | awk -F'"' '{if(NR%2 == 1) {printf $4} else {print ", "$4}}' > List_of_Districts.txt
