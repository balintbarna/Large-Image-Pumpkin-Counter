#!/bin/bash
cd ../2019-03-19\ Images\ for\ third\ miniproject/
array=($(ls))
printf "Extracting EXIF tool info \n" 
rm -f ../output/gps_pos.txt
for x in "${array[@]}"
do
	#exiftool "-DateTimeOriginal" $x
	exiftool "-GPSPosition" $x >> ../output/gps_pos.txt
	#exiftool "-GPSAltitude" $x
done
python3 ../src/makekml.py
