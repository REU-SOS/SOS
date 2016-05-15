

## set up

```sh
Me=someUniqueName
Tmp="/tmp/$USER/$$"
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
killControlM() { cat - | tr -d '\015'; } 
downCase()     { cat - | tr A-Z a-z; }
stemming()     { perl $Here/stemming.pl $1 ; }
stops()        { cat - | gawk ' 
       NR==1 {while (getline < Stops)  Stop[$0] = 1;
					        	while (getline < Keeps)  Keep[$0] = 1; 
					      	 }
					        { for(I=1;I<=NF;I++) 
					              if (Stop[$I] && ! Keep[$I]) $I=" "
                      print $0
				      	  }' Stops="$Here/stop_words.txt" \
					           Keeps="$Here/keep_words.txt" 
					        }
prep()  { cat - | killControlM | downCase | 
                  stemming | stops; }

```

## learning

Reads cooked data from `$Cooked`,

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
kill -9
```
For more details, see  http://www.tutorialspoint.com/unix/unix-signals-traps.htm.

