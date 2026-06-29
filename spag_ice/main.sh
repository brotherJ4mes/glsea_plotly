#!/bin/bash
echo =====================================================
echo "============    $(date "+%m-%d %H:%M")    ======================"
echo =====================================================
cd /home/kessler/plot_gen/spag_glsea/


# assign year and julian day based on todays date
#read -r yyyy mm jjj <<< $(date -d today "+%Y %m %j")


# call python script with year and jul. day so it knows which dat file to read
echo executing ./multi_lake.py...
python multi_lake.py

echo executing spaglotly.py...
echo sup mic hur eri ont | xargs -n1 python spaglotly.py 

# push json file to husky (update location soon)
#scp spag_compare_lks.json husky:/hump/glcfs/coastwatch_hack/
echo 'quietly pushing to husky... (0 => success)'
#scp -q *.json *.png husky:/hump/cwdata/wordpress-export/
scp -q *.json husky:/hump/glcfs/coastwatch_hack/
echo $?
scp -q html/* husky:/hump/WAF/data/glsea_maps/
echo $?





