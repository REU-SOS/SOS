

## set up

```bash
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
downCase() { cat - | tr A-Z a-z; }
stemming()  { perl $Here/stemming.pl $1 ; }

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

