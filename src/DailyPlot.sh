#!/bin/bash

Day=$(date +%d-%b) 
gnuplot <<- EOF	
	set xlabel "TIME"
	set ylabel "TEMPERATURE"
	set yrange [15:]
	set ytics 15,.5
	set terminal png size 1000,1000 enhanced font "Helvetica,20"
	set output "$Day.png"
	set border 3
	set tics nomirror out scale 0.75
	plot "./DataFile.dat" title 'Temperature Evolution ${Day}' with line
EOF
