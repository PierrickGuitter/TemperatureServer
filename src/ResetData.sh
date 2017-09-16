#!/bin/bash

Day=$(date +"%d-%b")
cp /root/$Day.png /var/www/temperature.png
mv /root/${Day}.png /root/TMP
rm /root/DataFile.dat
