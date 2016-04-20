#GENIC

One-pass incremental clustering.

[Read paper](http://goo.gl/rOFlvA). Reference:

```
INPROCEEDINGS{Gupta04genic:a,
    author = {Chetan Gupta and Robert Grossman},
    title = {GenIc: A Single Pass Generalized Incremental Algorithm for Clustering},
    booktitle = {In SIAM Int. Conf. on Data Mining},
    year = {2004},
    publisher = {SIAM}
}
```

## Exercise for Reader

Discovered... late at night... bug... this code throws away all but one cluster
at each generation...function of this data... bug?


## Install

Requires gawk 3 or higher.

Download:

+ [genic.awk](genic.awk)
+ [diabetes.csv](diabetes.csv)

Test:

```
gawk -f genic.awk diabetes.awk
```

You should see some output that looks like:

```
6,80,80,36,0,39.8,0.177,28,tested_negative
10,115,0,0,0,0,0.261,30,tested_positive
2,127,46,21,335,34.4,0.176,22,tested_negative
4,118,70,0,0,44.5,0.904,26,tested_negative
2,122,76,27,200,35.9,0.483,26,tested_negative
6,125,78,31,0,27.6,0.565,49,tested_positive
1,168,88,29,0,35,0.905,52,tested_positive
2,129,0,0,0,38.5,0.304,41,tested_negative
4,110,76,20,100,28.4,0.118,27,tested_negative
```

Which is to same, Genic went hunting through 700+ records to find (say) 20 clusters,
but found only nine
interesting ones.

## Tour of the code

### Set up stuff

```awk
BEGIN {
    FS=","; # columns sperated by ","
    K= 10 # initial number of centers
    M= 20 # number of initial points
    N=100 # size of one generation
    C=0   # cluster id
    Missing="?"
    split("",W,"")
}
```

### Stuff for every line

Kill white space and comments.

```awk
 {  gsub(/[ \t]/,"");  #kill white space
                gsub(/\#.*/,"")    #kill comments
 }
```

### Stuff for first line

Reset the random number seed, if supplied. Read the header

```awk
NR==1  {  srand(Seed ? Seed : 1)
          for(I=1;I<=NF;I++) 
                 readHeader(I,$I)
          next }

function readHeader(pos,val ) {
    if (gsub(/\$/,"",val)) { Num[pos] } else { Sym[pos]   }
    if (gsub(/\!/,"",val)) { Dep[pos] } else { Indep[pos] }
    Name[ pos] = val
    Index[val] = pos
}
```

Note that _readHeader_ creates arrays that have keys for each number,
symbol, dependent, independent col position (in _Num,Sym,Dep,Indep_
respectively).

### For every line after line one

Skip blank lines; update our knowledge of min and max for each column.


```awk
/^$/          { next }
              { for(I in Num) minMax(I,$I) }

function minMax(pos,val) {
    if(pos in Min) { if(val < Min[pos]) {Min[pos]=val} else {Min[pos]=val}}
    if(pos in Max) { if(val > Max[pos]) {Max[pos]=val} else {Max[pos]=val}}
}
```

### Finally, we get to Genic

#### New Centroids

The list _W_ has one index per centroid. If we have less than the
desired _K_ centroids, grab the next line and make it a centroid.

```awk
length(W) < K { more() }

function more( i) {
    while(length(W) < K) {
	C++
	W[C]=1
    	for(i=1;i<=NR;i++) Centroid[C,i]=$i
	next
    }
}
```

#### Moving Centroids to New Input

Now, move the current line to the nearest centroid (increasing the weight
of that centroid by "one".

Note in the following code, we move numbers and symbolic columns differently:

+ New nums in the moved centroid are the weighted sum of the new num and the
old centroid  nums (where "weight" comes from _W_).
+ New syms are the moved centroid is the new value, at probability _1/W_.

```awk
{ move(nearest()) }

function nearest(   min,c,tmp,out) {
	min = 1000
	for(c in W) 
		if((tmp = dist(c)) < min) {
			min = tmp
			out = c }
	return c
}

function move(c) {
	for(i=1;i<=NF;i++) {
		if (Centroid[c,i] == Missing)
			Centroid[c,i] == $i
		else if ($i != Missing)
			Centroid[c,i] = (i in Num) ? moveNum(c,i,$i) : moveSym(c,i,$i)
	}
	W[c]++
}
function moveNum(c,pos,val) {
	return (Centroid[c,pos]*W[c] + val)/(W[c]+1)	
}
function moveSym(c,pos,val) {
	if (rand() < 1/W[c])
		Centroid[c,pos] = val
}
```

As to the _nearest_ function, this is the classic Euclidean distance function.
Numbers are normalized 0..1 for min..max. Symbols have distance zero or one
(if they are same or different).  If there are any missing values,
assume max possible distance.

```awk
function dist(c,    y,n, i,out) {
	for(i in Indep) {
		n++
		y = Centroid[c,i]
		out+=(i in Num) ? distNum(norm(i,$i),y)^2 : distSep($i,y)^2 
	}
	return sqrt(out)/sqrt(n+0.0000001)
}
function norm(pos,val) {
    return (val - Min[pos]) / (Max[pos] - Min[pos] + 0.00001)
}
function distSym(x,y) {
	if (x == Missing) return 1
	if (y == Missing) return 1
	return x == y ? 0 : 1
}
function distNum(x,y) {
    if (x == Missing && y == Missing) return 1
    if (x == Missing) return y < 0.5 ? 1 - y : y
    if (y == Missing) return x < 0.5 ? 1 - x : x
    return x - y
}
```

#### Every N records, Throw Away Dull Centroids

Selected probabilistic. If a centroid has not attracted enough
rows, then we throw it away. Note that if we end up with less than
_K_ centroids, the above _New Centroids_ code will wake up and grab
the newt few rows for new centroids.

```awk
(NR % N) == 0 { less() }

function less(   sum,c,doomed) {
	for(c in W) sum += W[c]
	for(c in W) if (W[c]/sum < rand()) doomed[c]
	for(c in doomed) {
		delete W[c]
		for(i=1;i<=NR;i++) delete Centroid[c,i]
	}	
	for(c in W) W[c] = 1
}
```
### Finally, Print the Centroids

```awk
END           { printC() }

function printC(   c,i,str,sep) {
    for(c in W) {
	str=sep=""
        for(i=1;i<=NF;i++) {
            str = str sep Centroid[c,i]
            sep = ","
        }
        print str
    }
}
```

### Misc debug routine: Prints arrays

```awk
function o(a,str,     i,com) {
    com = "sort -k 2 #" rand()
    for(i in a) print str " [" i "]= "a[i] | com
    close(com)
} 
```
