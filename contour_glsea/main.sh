#!/bin/bash
echo =====================================================
echo "============    $(date "+%m-%d %H:%M")    ======================"
echo =====================================================
cd /home/kessler/plot_gen/contour_glsea/


# assign year and julian day based on todays date
read -r yyyy mm jjj <<< $(date -d today "+%Y %m %j")

if [ ! -f /mnt/cwdata/p/m/lcd/$yyyy/$mm/$yyyy_$jjj_glsea.asc ]; then
	echo no file for today... using yesterdays date
	read -r yyyy mm jjj <<< $(date -d yesterday "+%Y %m %j")
else
	echo found today!
fi


# call python script with year and jul. day so it knows which dat file to read
echo executing ./contour.py $yyyy $mm $jjj
./contour.py $yyyy $mm $jjj

# push json file to husky (update location soon)
echo 'quietly pushing to husky... (0 => success)'
scp -q out_json/*json husky:/hump/glcfs/coastwatch_hack/
echo $?
scp -q out_html/*.html husky:/hump/WAF/data/glsea_maps/
echo $?

#scp map_choro.png  /mnt/cwdata/webdata/glsea # doesn't update




