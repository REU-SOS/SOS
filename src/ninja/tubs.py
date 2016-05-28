"""

# tubs.py : tricks for storing columns of data.

(C) 2016 tim@menzies.us, MIT license

## Data model:

A `Tub` is a place to store columns of data:

- Columns contain either symbols or numbers.  

_ Columns have headers called `Sym` and `Num` and store summaires about
  symbolic or numeric columns, respectively.

- When a `Row` is dumped into a `Tub`, the column headers are automatically
  updated with information from that row

Important note:

- While `Row`s contain all the raw data, columns only contain a _summary_
  of the data seen in each column.
___________________________________________________________________________

"""

from __future__ import division,print_function
import sys,math
sys.dont_write_bytecode=True

from tricks import *

def isMissing(x):
  "Null cells in columns contain '?'"
  return x == "?"

"""________________________________________________________________________

## Col

`Col`s have two sub-classes: `Num` and `Sym`.

"""

class Col:
  def __init__(i,inits=[],get=same):
    i.reset()
    i._get = get
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    x = i._get(x)
    if not isMissing(x): i.add(x)
    return i
  def __isub__(i,x):
    x = i._get(x)
    if not isMissing(x): i.sub(x)
    return i
  def __repr__(i):
    return str(kv(i.__dict__))
  
class Sym(Col):
  """Incrementally adds and subtracts symbol counts as well the most common symbol
     (the 'mode'). Can report column 'entropy'."""
  def reset(i):
    i.counts, i.most, i.mode, i.n = {},0,None,0
  def add(i,x):
    i.n += 1
    new = i.counts[x] = i.counts.get(x,0) + 1
    if new > i.most:
      i.most, i.mode = new,x
  def sub(i,x):
    i.n -= 1
    i.counts[x] -= 1
    if x == i.mode:
      i.most, i.mode = None,None
  def k(i):
    return len(i.counts.keys())
  def ent(i):
    """Measures how many symbols are mixed up together.  If only one symbol, then
       ent=0 (nothing mixed up)."""
    tmp = 0
    for val in i.counts.values():
      p = val/i.n
      if p:
        tmp -= p*math.log(p,2)
    return tmp
      
class Num(Col):
  """Incrementally adds and subtracts numners to a Gaussian, tracking 'mu' and
     'sd()' as we go.  Smallest and largest values seen are 'lo' and 'up'.  Can
     report column 'standard deviattion'."""
  def reset(i):
    i.mu,i.n,i.m2,i.up,i.lo = 0,0,0,-10e32,10e32
  def add(i,x):
    """Incremental addition using ??Knuths 1964 method, see
       https://goo.gl/gk32eX."""
    i.n += 1
    if x < i.lo: i.lo=x
    if x > i.up: i.up=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    """During subtraction, if counts go negative, cap them at zero."""
    i.n   = max(0,i.n - 1)
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
  def sd(i):
    "Measures how varied are the measures from the mean."
    return 0 if i.n <= 2 else (i.m2/(i.n - 1))**0.5
  def small(i,cohen=0.3):
    return i.sd()*cohen

"""________________________________________________________________________

## Tub 

- When a new `Row` is added, updates column summaries.
- When processing a `Row`,  if a cell is empty (defined by `isMissing`) then we skip over it.
- The type of a column is defermined by the first non-empty entry seen in any row
  (see how `about` is set, below).
- Before summarizing a row in a column header, the row is filted via some `get`
  function (which defaults to `same`; i.e.  use the whole row, as is).

Note that `Tub`s do not store the `rows` (that is done elsewhere, see `TwinTub`, below).
"""

class Tub:
  def __init__(i,get = same):
    i.cols = {}  # i.cols[i] is a summary of column i.
    i._get = get
  def __iadd__(i,lst):
    lst = i._get(lst)
    for j,val in enumerate(lst):
      if not isMissing(val):
        col = i.cols.get(j,None)
        if not col:
          col = i.cols[j] = Sym() if isSym(val) else Num()
        col += val
    return i

"""________________________________________________________________________
# Row       

A `Row` is something that can be divided into into `x,y` columns and each of
 which can be stored in different tubs.  The knowledge of how to access `x`, or
 `y` out of the row is given to a `Tub` when it is created (see the above
 `Tub.get` attribute).

"""

class Row:
  def __init__(i,x=None,y=None):
    i.x = x or []
    i.y = y or []
    
"""________________________________________________________________________
## TwinTub
 
A `TwinTub` is a place to store `Row`s and summaries about those rows.
Those summaries are stored in two `Tub`s (hence the name "twin tub").

- The _x_ field holds a _Tub_ of any independent data;
- The _y_ field holds a _Tub_ of any dependent data (e.g. one of more class
  variables).
- When a row is added to a _TwinTub_, its_x,y_ components are sent to two
  seperate _Tubs_

First, need accessors to _x,y_ fields:

"""

def xx(z): return z.x
def yy(z): return z.y

class TwinTub:
  def __init__(i,xx=xx,yy=yy):
    i.x=Tub(xx)
    i.y=Tub(yy)
    i._rows = []
  def __iadd__(i,row): 
    i.x += row
    i.y += row
    i._rows += [row]
    return i

"""_______________________________________________________________________
## Arff

`Arff` is a class that reads a data file of the following form:

    @RELATION iris
    
    @ATTRIBUTE sepallength  NUMERIC
    @ATTRIBUTE sepalwidth   NUMERIC
    @ATTRIBUTE class        {Iris-setosa,Iris-versicolor,Iris-virginica}
  
    @DATA
    5.1,3.5,Iris-setosa
    4.9,3.0,Iris-setosa
    4.7,3.2,Iris-setosa
    ...

The `rows` after `@data` are stored in `TwinTubs` (where it is assumed the last
cell in each row is the class).  Other information is stored in a list of
`attributes` and the name of the `relation`.

The input rows from a file are all strings so first they are coerced to floats,
ints, or strings using `thing`.  Next, the coerced row is sent through a
customisable `filter` (which defaults to `same`).

Note that when reading the @XXX tags, `Arff` uses a case-insensitive match
(see the use of `re.IGNORECASE`, below).

"""
class Arff:
  def __init__(i, f, filter=same):
    i.tubs = TwinTub()
    i.attributes = []
    i.relation   = 'relation'
    i.filter     = filter
    i.reads(f)
  def empty(i,x):
    return re.match('^[ \t]*$',x)
  def at(i,x,txt):
    return re.match('^[ \t]*@'+txt,x,re.IGNORECASE)
  def header(i):
    return ", ".join(i.attributes)
  def reads(i,f):
    data = False
    with open(f)  as fs:
      for line in fs:
        line = re.sub(r'(["\'\r\n]|#.*)', "", line)
        if line:
          if not i.empty(line): # skip blank lines
            if data:
              line = line.split(",")
              line = i.filter(map(thing,line))
              indep= line[:-1]
              dep  = [line[-1]]
              i.tubs += Row(x=indep, y=dep)
            else:
              line = line.split()
              if i.at(line[0],'RELATION'):
                i.relation = line[1]
              elif i.at(line[0],'ATTRIBUTE'):
                i.attributes += [line[1]]
              elif i.at(line[0],'DATA'):
                data=True

"""_______________________________________________________________________
## demo

For example, consider the file `weather.arff`:

    @relation weather
    @attribute outlook     {sunny,  overcast, rainy}
    @attribute temperature real
    @attribute humidity    real
    @attribute windy       {TRUE , FALSE}
    @attribute play        {yes  , no}
    @data
    sunny,       85,         85,       FALSE,  no
    sunny,       80,         90,       TRUE,   no
    overcast,    83,         86,       FALSE,  yes
    rainy,       70,         96,       FALSE,  yes
    rainy,       68,         80,       FALSE,  yes
    rainy,       65,         70,       TRUE,   no
    overcast,    64,         65,       TRUE,   yes
    sunny,       72,         95,       FALSE,  no
    sunny,       69,         70,       FALSE,  yes
    rainy,       75,         80,       FALSE,  yes
    sunny,       75,         70,       TRUE,   yes
    overcast,    72,         90,       TRUE,   yes
    overcast,    81,         75,       FALSE,  yes
    rainy,       71,         91,       TRUE,   no


If we read this file and print the headers on the _x_ tub, we see the
distributions of symbols and numbers in the independent (non-class) columns.

{0: ["counts: {'rainy': 5, 'overcast': 4, 'sunny': 5}", 'mode: sunny', 'most: 5', 'n: 14'], 
 1: ['lo: 64', 'm2: 561.43', 'mu: 73.57', 'n: 14', 'up: 85'], 
 2: ['lo: 65', 'm2: 1375.21', 'mu: 81.64', 'n: 14', 'up: 96'], 
 3: ["counts: {'TRUE': 6, 'FALSE': 8}", 'mode: FALSE', 'most: 8', 'n: 14']}
}

"""
if __name__ == '__main__':
  a=Arff('data/weather.arff')
  print(a.tubs.x.cols)


