BEGIN {
    FS=","; # columns sperated by ","
    K= 20 # initial number of centers
    M= 20 # number of initial points
    N=100 # size of one generation
    C=0   # cluster id
    Missing="?"
    split("",W,"")
}
             {  gsub(/[ \t]/,"");  #kill white space
                gsub(/\#.*/,"")    #kill comments
             } 
NR==1        {  srand(Seed ? Seed : 1)
                for(I=1;I<=NF;I++) 
                    readHeader(I,$I)
		 next }
/^$/          { next }
              { for(I in Num) minMax(I,$I) }
length(W) < K { more() }
              { move(nearest()) } 
(NR % N) == 0 { less() }
END           { printC() }

function printC(   c,i,str,sep) {
    print ""
    print "records: ",NF
    print "centrods: ",length(W)
    for(c in W) {
	str=sep=""
        for(i=1;i<=NF;i++) {
            str = str sep Centroid[c,i]
            sep = ","
        }
        print str
    }
}
function more( i) {
   
    while(length(W) < K) {
	printf("+")
	C++
	W[C]=1
    	for(i=1;i<=NR;i++) Centroid[C,i]=$i
	next
    }
}
function less(   sum,c,doomed) {
   
	for(c in W) sum += W[c]
  	for(c in W) {
	    #print W[c],sum,W[c]/sum
            if (W[c]/sum < rand()) doomed[c]
        }
	for(c in doomed) {
	    printf("-")
	    delete W[c]
	    for(i=1;i<=NR;i++) delete Centroid[c,i]
	}
	print ""
	#for(c in W) W[c] = 1
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
function nearest(   min,c,tmp,out) {
	min = 1000
	for(c in W) 
		if((tmp = dist(c)) < min) {
			min = tmp
			out = c }
	return c
}
function dist(c,    y,n, i,out,d) {
	for(i in Indep) {
		n++
		y = Centroid[c,i]
		out+=((i in Num) ? distNum(norm(i,$i),y)^2 : distSep($i,y)^2)
	}
	d=sqrt(out)/sqrt(n+0.0000001)
	return d
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
function minMax(pos,val) {
    if(pos in Min) { if(val < Min[pos]) {Min[pos]=val} else {Min[pos]=val}}
    if(pos in Max) { if(val > Max[pos]) {Max[pos]=val} else {Max[pos]=val}}
}
function norm(pos,val) {
    return (val - Min[pos]) / (Max[pos] - Min[pos] + 0.00001)
}
function readHeader(pos,val ) {
    if (gsub(/\$/,"",val)) { Num[pos] } else { Sym[pos]   }
    if (gsub(/\!/,"",val)) { Dep[pos] } else { Indep[pos] }
    Name[ pos] = val
    Index[val] = pos
}
function o(a,str,     i,com) {
    com = "sort -k 2 #" rand()
    for(i in a) print str " [" i "]= "a[i] | com
    close(com)
} 
