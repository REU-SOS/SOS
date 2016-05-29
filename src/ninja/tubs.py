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
Demos=[]

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

Note that `Tub`s do not store the `rows` (that is done elsewhere, see `Tubs`, below).
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
          col.pos = j
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
## Tubs
 
A `Tubs` is a place to store `Row`s and summaries about those rows.
Those summaries are stored in two `Tub`s.

- The `x` field holds a `Tub` of any independent data;
- The `y` field holds a `Tub` of any dependent data (e.g. one of more class
  variables).
- When a row is added to a `Tubs`, its `x,y` components are sent to two
  seperate _Tubs_

First, need accessors to _x,y_ fields:

"""

def xx(z): return z.x
def yy(z): return z.y

class Tubs:
  def __init__(i,xx=xx,yy=yy):
    i.x=Tub(xx)
    i.y=Tub(yy)
    i._rows = []
  def __iadd__(i,row):
    i.x += row
    i.y += row
    i._rows += [row]
    return i
  def col(i,pos):
    if  pos < len(i.x.cols):
      return i.x.cols[pos]
    else:
      return i.y.cols[len(i.x.cols) - pos ]
  def cell(i,row,pos):
     if  pos < len(i.x.cols):
      return row.x[pos]
     else:
      return row.y[len(i.x.cols) - pos]

