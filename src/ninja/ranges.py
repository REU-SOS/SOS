"""

# ranges.py : tricks for dividing numeric columns into a few ranges

(C) 2016 tim@menzies.us, MIT license

"""

from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True

from tubs import *

"""
## Top-Down Bi-Clustering

All the following tricks us the same top-down bi-clustering approach:

- Sort the rows by some column
- Run down the sorted column looking for the _best_ place to break the column in two.
      - Where _best_ might mean many things, discussed below.
- Recurse into both breaks.

These tricks divides a column into a list of useful `Range`s. The most important
part of the following class is the `pretty` method that lets us show a range as 
some region between some values.
"""

class Range:
  def __init__(i, attr=None, n=None,  lo=None,  report=None,
                  id=None,   up=None, has=None, score=None):
    i.attr, i.lo, i.up, i._has = attr, lo, up, has
    i.score, i.n, i.id         = score, n, id
    i.report=report
  def __repr__(i):
    return str(kv(i.__dict__))
  def pretty(i)  :
    if i.lo == i.up:
      return str(i.lo)
    else:
      return '[%s..%s]' % (i.lo,i.up)
  
"""

## Dull Columns and Irrelevant Ranges

In the following,two  important events are 

- When these tricks divide a column into one, and only one, `Range`. We call such
  a column _dull_ since it means 
  means that we were unable to find useful structure within a column.
       + Note that the opposite of dull is `sharp`.
- When a `Range` is _irrelevant_; i.e. it does
  not contain a majority of whatever effect is desired.
       + Note that the opposite of irrelevant is `relevant`. 

As shown below, by ignoring dull columnns and irrelevant ranges,
seemingly
complex data sets can be summarised in just a few ranges.

## Sanity Steps:

Note that all these tricks use four sanity tricks:

- Don't waste time resorting the columns for every level of the recursion:
       - Sort the whole column once, at the start, then pass the sorted sub-ranges into
         the recursive calls.
- Don't break things into sub-ranges with two few samples
       - E.g. with less than the square root of the number of items in the column;
       - This is controlled by the `enough` parameter.
- Don't break things into sub-ranges just cause of some small effect
       - E.g. if the standard deviation of the entire column is `sd` and
         some range streches from `lo` to `up`, then not break into sub-ranges 
         where `(up - lo)` is less than `0.2*sd`.
       - This is controlled by the `cohen` parameter and, by default, `cohen=0.2`.
- Each sub-range must be more that trivially better than the current range
       - E.g. at least 5% better
       - This is controlled by the `trvial` parameter and, by default `trivial=1.05`.
- When checking where to break up a range, use two counters:
       - One `lhs` counter for the information up to some position `i`;
       - One `rhs` counter for the information from `i` to the end 

As to that last point, initially `lhs` is empty and `rhs` contains information
about the entire lst. Then we walk over the sorted list, adding in each item
to `lhs` while removing it from `rhs`. This means that a skeleton template for
all the following code looks like this:


   def div(lst):
     divide(sorted(lst),      # only sort once
            trivial = 1.05,
            small   = rhs.sd()*0.2,
            enough  = sqrt(len(lst)))

   def divide(lst, trivial, small, enough, cut=None) :
     lhs, rhs = nothing, everything(lst)
     score    = some initial value
     for i,new  in enumerate(lst):
       lhs += new                      # lhs is a `Col` and supports `__iadd__`
       rhs -= new                      # rhs is a `Col` and supports `__isub__`
       if rhs.n < enough:              # break when too few rhs samples
         break
       else:
        if lhs.n >= enough:            # wait till enough lhs samples
          start, here, stop = lst[0], new, lst[-1]
          if here - start > small:     # ignore small effects
            if stop - here > small:    # ignore small effects
               score1 = something
               if score1 * trivial < score: # ignore trivial differences.
                  score, cut = score1, i
     return cut, score # cut is None if no breaks found

XXX explain this is a greedy search but, heh, its fayyad iranni so chill

One more trick, then we can look at the code:

- Sometimes, in the following, we work with _pairs_ of columns looking for
  breaks in column1 such that it most divides up the associated values in column2.
- Hence, in the following, all the `divide` codes have accessors `xx` and `yy`
  telling it what column to break on (the `xx` ones) in order to have most
  effct on the  other column `yy`. 
- For the simple case, where we are just dividing a column without reflecting
  on any other column, we just set ``yy=xx`` (e.g. see `sddiv`, below).

__________________________________________________________________________
## Configuration Options

"""

The.divs = o(attr    = 0,      # a label for the ranges
             cohen   = 0.2,    # 'small' means sd()*cohen
             trivial = 1.05,   # need at least a 5% improvement
             enough  = None,   # enough items for a bin. default=n**0.5
             small   = None,   # when are numbers too small?
             verbose = False)

"""_____________________________________________________________________
## sdiv: Dividing Numeric Columns

- `cohenPrune` divides one column into ranges of width not smaller than some
  fraction of the standard deviation.
- `sdPrune` that divides one column in to ranges that minimize the expected
  deviation of that same column.
- `sdiv` that divides the `xx` column such that it minimizes the expected
  deviation of the `yy` column.

Note that `cohenPrune` and `sdPrune` are just special ways to call `sdiv`.

"""

def cohenPrune(lst,**d): return sdPrune(lst, minSd=False, **d)
def sdPrune(   lst,**d): return sdiv(   lst, yy=d['xx'],  **d)

def sdiv(lst,
         attr    = The.divs.attr,     # a label for the ranges
         cohen   = The.divs.cohen,    # 'small' means sd()*cohen
         trivial = The.divs.trivial,  # need at least a 5% improvement
         enough  = The.divs.enough,   # enough items for a bin. default=n**0.5
         small   = The.divs.small,    # when are numbers too small?
         verbose = The.divs.verbose,  # prints some trace info
         xx      = same,   # access independent variable
         yy      = same,   # access dependent   variable
         minSd   = True):  
  # ---------------------------------------------------
  def divide(lst, out=[], lvl=0, cut=None):
    xlhs, xrhs   = Num(get=xx), Num(lst, get=xx)
    ylhs, yrhs   = Num(get=yy), Num(lst, get=yy)
    score,score1 = yrhs.sd(),None
    n            = len(lst)
    report       = copy(yrhs)
    for i,new in enumerate(lst):
      xlhs += new; xrhs -= new
      ylhs += new; yrhs -= new
      if xrhs.n < enough:
        break
      else:
        if xlhs.n >= enough:
          start, here, stop = xx(lst[0]), xx(new), xx(lst[-1])
          if here - start > small:
            if stop - here > small:
              if minSd:
                score1 = ylhs.n/n*ylhs.sd() + yrhs.n/n*yrhs.sd()
                if score1*trivial < score:
                  cut,score = i,score1
              else:
                cut,score = i,score1
    # --- end for loop -------------------------------
    if verbose:
      print('.. '*lvl,len(lst),score1 or '.')
    if cut:
      divide(lst[:cut], out= out, lvl= lvl+1)
      divide(lst[cut:], out= out, lvl= lvl+1)
    else:
      out.append(Range(attr=attr, score=score, report=report,
                       n=len(lst), id=len(out),
                       lo=xx(lst[0]), up=xx(lst[-1]),
                       has=lst))
    return out
  # --- end function div -----------------------------
  if not lst: return []
  small  = small  or Num(lst,get=xx).small(cohen)
  enough = enough or len(lst)**0.5
  return divide( sorted(lst[:], key=xx), out=[] ,lvl=0) # copied, sorted


"""_____________________________________________________________________
## ediv: Dividing Symbolic Columns

This code divides a numeric column in such a way that each range
selects for very few (perhaps, just one) symbol in another column.

The spread of symbols is measured by `entropy` which is a measure
of how many different symbols fall into some set (and a set with only
one symbol has entropy of zero).

This code contains some funky information theory tricks (see `delta`
and `border` below) to determine a stopping criteria
for the recursion.  For details on those tricks, see
http://robotics.stanford.edu/users/sahami/papers-dir/disc.pdf

XXX Fayyad irrani

"""  

def ediv(lst,
         attr    = The.divs.attr,
         cohen   = The.divs.cohen,
         trivial = The.divs.trivial,
         enough  = The.divs.enough,
         small   = The.divs.small,
         verbose = The.divs.verbose,
         xx      = xx,
         yy      = yy):
  def divide(lst, out=[], lvl=0, cut=None):
    def ke(z): return z.k()*z.ent()
    cut            = None
    xlhs, xrhs     = Num(get=xx), Num(lst, get=xx)
    ylhs, yrhs     = Sym(get=yy), Sym(lst, get=yy)
    k0, e0, ke0    = yrhs.k(), yrhs.ent(), ke(yrhs)
    score,score1   = yrhs.ent(),None
    report         = copy(yrhs)
    n = len(lst)
    for i,new  in enumerate(lst):
      xlhs += new; xrhs -= new
      ylhs += new; yrhs -= new
      if xrhs.n < enough:
        break
      else:
        if xlhs.n >= enough:
          start, here, stop = xx(lst[0]), xx(new), xx(lst[-1])
          if here - start > small:
            if stop - here > small:
              score1= ylhs.n/n*ylhs.ent()+ yrhs.n/n*yrhs.ent()
              if score1*trivial < score:
                gain   = e0 - score1
                delta  = math.log(3**k0-2,2)-(ke0- ke(yrhs)-ke(ylhs))
                border = (math.log(n-1,2) + delta)/n
                if gain >= border:
                  cut,score = i,score1
  #----------------------------------------------
    if verbose:
      print('.. '*lvl,len(lst),score1 or '.')
    if cut:
      divide(lst[:cut], out=out, lvl=lvl+1)
      divide(lst[cut:], out=out, lvl=lvl+1)
    else:
      out.append(Range(attr=attr, score=score, report=report,
                       n=len(lst), id=len(out),
                       lo=xx(lst[0]), up=xx(lst[-1]),
                       has=lst))                       
    return out
  #---| main |-----------------------------------
  if not lst: return []
  small  = small  or Num(lst,get=xx).small(cohen)
  enough = enough or len(lst)**0.5
  return divide(sorted(lst,key=xx), out=[], lvl=0)

"""________________________________________________________________

## Demo code

"""

def _sdiv():
  rseed(1)
  n   = 1000
  lst = [r()**2 for x in xrange(n)]
  lst = lst + [r()**0.5 for x in xrange(n)]
  for y in sdiv(lst):
    print(y)
 
def _ediv():
  rseed(1)
  lst1 = list("abcd")
  lst2 = []
  for _ in xrange(1000):
    for i,x in enumerate(lst1):
      lst2 += [[i+0.5*r(), x]] # 'a' is around 0.5, 'd' is around 3.5
  lst2 = sorted(lst2)
  for y in ediv(lst2,
                xx=lambda z: z[0],
                yy=lambda z: z[1]):
    print(y)

if __name__ == "__main__":
  _sdiv()
  print("")
  _ediv()
