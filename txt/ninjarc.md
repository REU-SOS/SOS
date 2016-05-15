Mined from many different log files. Written, not run. Send bug reports to tim@menzies.us

## debgging

Usuaully, run with the following line uncommented.

```
#set -x
set -e # if anything terminates with an error, halt right awy
```

## set up

```sh
Me=someUniqueName
Tmp="/tmp/$USER/$$" # some places, /tmp is size restricted. Here, you want some place BIG
Safe="$HOME/tmp/safe/$Me"

## Raw = source of raw data; Cooked= pre-processed stuff
Raw=somePath
Cooked="$Safe/someOtherPath"

## java libraries
Jar="$HOME/svns/wisp/trunk/weka/lib/weka.jar"
Weka="java-Xmx1024M -cp $Jar "

dirs() {
 	mkdir -p $Safe $Temp
}
```

## slow cooking

One-time pre-processing. Results stored in `$Cooked`.

```
killControlM() { tr -d '\015'; } 
downCase()     { tr A-Z a-z; }
stemming()     { perl $Here/stemming.pl  ; }
stops()        {  gawk ' 
       NR==1 {while (getline < Stops)  Stop[$0] = 1;
					        	while (getline < Keeps)  Keep[$0] = 1; 
					      	 }
					        { for(I=1;I<=NF;I++) 
					              if (Stop[$I] && ! Keep[$I]) $I=" "
                      print $0
				      	  }' Stops="$Here/stop_words.txt" \
					           Keeps="$Here/keep_words.txt" 
					        }
prep()  { killControlM | downCase | 
                  stemming | stops; }

f=demo.txt
prep < $f
```

## learning

Reads cooked data from `$Cooked`,

## reporting

Converts tab-seperated data in  `fred.dat` to `fred.pdf`

```bash
plot() {
  gnuplot <<EOF
    set nokey
    set terminal postscript eps "Helvetica" 20 # eps means "dont fill page"
    set size 0.5,0.5            # small graph, half page wid"
    set title "TF*IDF [$i]"
    set logscale y
    set output "$Safe/$i.eps"
    set xtics rotate
    plot "$i.dat" using 1:3 # just us columns one and 3
EOF
  ps2pdf $Safe/$i.eps  # generated pdf
}

plot fred
```



For more on gnuplot, see 

+ http://www.gnuplot.info/
+ http://folk.uio.no/hpl/scripting/doc/gnuplot/Kawano/index-e.html

![http://gnuplot.sourceforge.net/demo_4.6/using.2.png](http://gnuplot.sourceforge.net/demo_4.6/using.2.png)

For alternatives to gnuplot, consider:

+ Matplotlib
+ "R"
+ Javascript: http://www.sitepoint.com/15-best-javascript-charting-libraries/. D3.js is very popular right now.



## clean up

```
function cleanUp() {
    if [[ -d "Tmp" ]]
    then
        rm -r "$Tmp"
    fi
}
```

## Trap to always clean

Trap normal exit, interrupts etc.
```
trap cleanUp 1 2 3 4 15
```

+ 1	= Hang up detected on controlling terminal or death of controlling process
+ 	2	= Issued if the user sends an interrupt signal (Ctrl + C).
+ 	3	=  Issued if the user sends a quit signal (Ctrl + D).
+ 4 = 	Issued if an illegal mathematical operation is attempted
+ 15 = 	Software termination signal (sent by kill by default).


For a list of all traps,  on your system...
````
kill -l
```
For more details, see  http://www.tutorialspoint.com/unix/unix-signals-traps.htm.

