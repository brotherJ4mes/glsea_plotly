#!/bin/bash
echo =====================================================
echo "============    $(date "+%m-%d %H:%M")    ======================"
echo =====================================================
cd /home/kessler/plot_gen/map_glsea/


# assign year and julian day based on todays date
read -r yyyy mm jjj <<< $(date -d today "+%Y %m %j")

if [ ! -f /mnt/cwdata/p/m/lcd/$yyyy/$mm/$yyyy_$jjj_glsea.dat ]; then
	echo no file for today... using yesterdays date
	read -r yyyy mm jjj <<< $(date -d yesterday "+%Y %m %j")
else
	echo found today!
fi


# call python script with year and jul. day so it knows which dat file to read
echo executing ./choro.py $yyyy $mm $jjj
./choro.py $yyyy $mm $jjj

# push json file to husky (update location soon)
echo 'quietly pushing to husky... (0 => success)'
scp -q map_choro.json husky:/hump/glcfs/coastwatch_hack/
echo $?
#scp -q map_choro.html husky:/hump/WAF/data/glsea_maps/
#echo $?

#scp map_choro.png  /mnt/cwdata/webdata/glsea # doesn't update




