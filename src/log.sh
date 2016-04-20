#!/bin/bash
#/* vim: set filetype=sh ; */
#This is a log of Tim Menzies exploring issue reports from PITS.

Files="a b c d e"
#Files="a"

# home
Align="align -s/, -g 1";
Root="$HOME/svns"; Weka="$HOME/svns/wisp/trunk/weka/lib/weka.jar"

#nasa
#Align="malign"; Root=$HOME/work; Weka="/cygdrive/i/timm/svns/wisp/trunk/weka/lib/weka.jar"

Dir=$Root/mine/trunk/doc/07/telling/data/raw 
Safe=~/tmp/textmine/safe
Temp=~/tmp/textmine/tmp
Here=`pwd`

dirs() {
	[ -d $Temp ] &&  rm -r $Temp
	mkdir -p $Safe $Temp
        ls $Temp
}
#Q: how to get the data out of excel?
#Done: export as tab delimited into three project  l.txt p.txt s.txt

#Q: is the data "clean"
#Do: cat files, look for funny characters
#Note: found some stray "Ã", stored it in "bad.txt"

lowerCase() { gawk '{
					gsub(/A/,"a"); 
					gsub(/B/,"b"); 
					gsub(/C/,"c"); 
					gsub(/D/,"d"); 
					gsub(/E/,"e"); 
					gsub(/F/,"f"); 
					gsub(/G/,"g"); 
					gsub(/H/,"h"); 
					gsub(/I/,"i"); 
					gsub(/J/,"j"); 
					gsub(/K/,"k"); 
					gsub(/L/,"l"); 
					gsub(/M/,"m"); 
					gsub(/N/,"n"); 
					gsub(/O/,"o"); 
					gsub(/P/,"p"); 
					gsub(/Q/,"q"); 
					gsub(/R/,"r"); 
					gsub(/S/,"s"); 
					gsub(/T/,"t"); 
					gsub(/U/,"u"); 
					gsub(/V/,"v"); 
					gsub(/W/,"w"); 
					gsub(/X/,"x"); 
					gsub(/Y/,"y"); 
					gsub(/Z/,"z"); 
					print $0;
					}
                    ' $1
}
stops()     { gawk ' NR==1 {  
						while (getline < Stops)  Stop[$0] = 1;
						while (getline < Keeps)  Keep[$0] = 1; 
						}
					 { for(I=1;I<=NF;I++) if (Stop[$I] && ! Keep[$I]) $I=" "
                       print $0
					 }'                             \
					  Stops="$Here/stop_words.txt" \
					  Keeps="$Here/keep_words.txt"  \
					 $1
		    }
stemming()  { perl $Here/stemming.pl $1 ; }

#Do: remove the stray
cleans() {
	for i in $Files; do
		(
		cd $Dir; clean tab${i}5.csv 2> /dev/null | 
		lowerCase | tee $Temp/$i.allWords | 
		stops     | tee $Temp/$i.stopped  |
		stemming  | tee $Temp/$i.stemmed  |
		gawk -F, '$3 {OFS=","; print $4 "," $3 "\n"}' >  $Temp/ok_$i
		)
	done
}
tfidfs() {
	echo a ; (cd $Temp; tfidfs1 a 2);
	echo b ; (cd $Temp; tfidfs1 b 2);
	echo c ; (cd $Temp; tfidfs1 c 3);
	echo d ; (cd $Temp; tfidfs1 d 3);
	echo e ; (cd $Temp; tfidfs1 e 2);
}
#function prune() {
#    gawk '/[a-z]/{print $0}' -
#}
tfidfs1() {
	i=$1
	cut -d, -f 1 ok_${i} |  tfidf | sort  -n -r -k 2 | cat -n >   $i.dat	
	cat $i.dat | gawk '/[a-z]/ {print $0}'  | head -100  | cut -f 2  > $i.top100 
	gnuplot <<EOF
	set nokey
	set terminal dumb
	set logscale y
	set output "$i.plt"
	plot "$i.dat" using 1:3
EOF
	gnuplot <<EOF
	set nokey
	set terminal postscript eps "Helvetica" 20
		set size 0.5,0.5
		set title "TF*IDF [$i]"
	set logscale y
	set output "$i.eps"
		set xtics rotate
	plot "$i.dat" using 1:3
EOF
	epstopdf $i.eps
	cat $i.plt

	cat ok_${i} |
	gawk -F, ' 
	NR ==1 { while (getline < Powerful)  Want[$0] = 1;
	for(I in Want) 
		printf("%s,",I); 
		print "severity"
	}
	NR > 1 { gsub(/ /,"",$2);  counts($1,Want,  $2) }
	function counts(str,want,klass,   sum,out,i,j,n,tmp,got) {
	n=split(str,tmp," ");
	for(i=1;i<=n;i++) 
		if (tmp[i] in want) 
			got[tmp[i]]++;
			for(j in want) {
				sum += got[j]
				out = out got[j]+0 ",";  
			}
			if (sum)
				print out "_" klass   
			}
			'    Max=$2    Powerful="$i.top100"  > $i.csv
		}

tfidf() { gawk  -f $Here/tfidf.awk --source '{train() }
                   END {OFS=","; for(I in Word)  printf("%s\t %20.20f\n", I, tfidf(I)) } ' $1 ; } 
cat <<'EOF' >tfidf.awk 
function train()  {
	Documents++;
	for(I=1;I<NF;I++) {
              
		if( ++In[$I,Documents]==1) 
			Document[$I]++
				Word[$I]++
				Words++ }
}
function tfidf(i) { return Word[i]/Words*log(Documents/Document[i]) }
EOF

clean() {
	gawk '{gsub(Bad,""); print $0}' Bad=`cat $Here/bad.txt` $1 |
	sed 's/[\"\.\*\/\\\(\)\{\}\[\]><\(\)]/ /g'   
}
#clean1
#Note: project data is now in ok_l.txt ok_p.txt ok_s.txt

#Do: look for corrupt records
countFieldsRecords() {
	for i in $Temp/ok*; do
		gawk -F, '{print FILENAME " " NF}' $i 
  	done  | sort | uniq -c
}
#countFieldsRecords
# ==>
#   1 ok_bad.txt 0
# 155 ok_l.txt 11
# 773 ok_p.txt 11
#4661 ok_s.txt 9

#Note: project s has two less records for "phase found and phase introduced" 
#Do: using excel, move the columns only found in l and p to end of line

#Q: what are the fields
fieldNames() {
 #for i in ok_*.txt; do gawk -F"\t" 'NR==1{for(i=1;i<=NF; i++) print i " " $i}' $i done
 echo "Description"
 echo "Severity"
}
#Q: what are the severities?
contents() {
 for i in $Temp/ok_? ; do 
	 printf "\n\n---| $i |---------------\n"
	 gawk -F, '{x[$2]++} END {for(i in x) print "["i"] " x[i]}' $i |  $Align | sort
	 #gawk -F"\t" 'NR !=1 && NF > 8{if($Goal) print $Goal }' Goal=$2 $i |
 	#gawk '{x[$1]++; n++} END {OFS=",";for(i in x) print i,x[i],int(x[i]*100/n)}' |  malign |sort
 done  
 }
# severities

# ---| /Users/timm/tmp/textmine/tmp/ok_a |---------------
# [2] 311
# [3] 356
# [4] 208
# [5] 26
# 
# ---| /Users/timm/tmp/textmine/tmp/ok_b |---------------
# [2] 23
# [3] 523
# [4] 382
# [5] 59
# 
# ---| /Users/timm/tmp/textmine/tmp/ok_c |---------------
# [3] 132
# [4] 180
# [5] 7
# 
# ---| /Users/timm/tmp/textmine/tmp/ok_d |---------------
# [2] 1
# [3] 167
# [4] 13
# [5] 1
# 
# ---| /Users/timm/tmp/textmine/tmp/ok_e |---------------
# [2] 24
# [3] 517
# [4] 243
# [5] 41
# 
#Note: i have no insights from "domain"
#dates

# after much curve fitting, can't find a curve that correlates well with the data (much noise)


learn() {
	X=$1
	cd $Temp
	cp $HOME/svns/wisp/trunk/weka/lib/weka.jar $Temp
	java -cp ./weka.jar weka.core.converters.CSVLoader $X.csv > $X.arff
	java   -Xmx1024M -cp ./weka.jar \
		weka.filters.supervised.attribute.AttributeSelection \
	    -S "weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1"  \
	    -E  "weka.attributeSelection.InfoGainAttributeEval"                    \
	    -i  $X.arff \
		-o ${X}_fs.arff

	grep "@" ${X}_fs.arff | gawk '{print $2}' | tee $Safe/$X.order
	for i in 100 50 25 12 6 3
	do
		printf "\n\n---| $X $i  |------------------------\n\n"
		java  $java  -Xmx1024M -cp ./weka.jar \
			weka.filters.unsupervised.attribute.Remove  -R "${i}-100" \
			-i ${X}_fs.arff  \
			-o ${X}_fs${i}.arff
		printf "learning...\n\n"
		java  $java  -Xmx1024M -cp ./weka.jar \
			weka.classifiers.rules.JRip -F 3 -N 2.0 -O 2 -S 1 \
			-i -t  ${X}_fs${i}.arff |
		gawk  'BEGIN { RS=""} {N++; R[N]=$0} 
			   END   { print R[3]; print ""; 
			           print R[17]; print "";  print R[15]}' 
	done | tee $X.log
}
#========
# preliminary investigations only offer one insight (the leakage numbers).
# see txtlog.sh for the data mining stuff

start() {
dirs
cleans
countFieldsRecords
contents
tfidfs
for i in $Files; do
    cp $Temp/$i.plt $Safe
    cp $Temp/$i.pdf $Safe
done
}

learns() {
 


 learn a  ; cp $Temp/a.log $Safe
 learn b  ; cp $Temp/b.log $Safe
 learn c  ; cp $Temp/c.log $Safe
 learn d ; cp $Temp/d.log $Safe
 learn e  ; cp $Temp/e.log $Safe
}

PS1="TEXT> "
#start
#learns
