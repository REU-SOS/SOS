"""

# discretize.py : tricks for dividing numeric columns into a few ranges

(C) 2016 tim@menzies.us, MIT license

"""

from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True

from arff import *
Demos=[]

"""## What is Discretization?

<img 
src="https://lh3.ggpht.com/7QvF4vsk9kWBelRvKJpD6LfnKgSzwH9OLykZDs1GQFsgQ1-nbaMPPZ4MIkp3PM5b3g=w300" 
align=right>

Think of learning like an accordion- some target concept is spread out across
all the data and our task is to squeeze it together till it is dense enough to
be visible. That is, learning is like a compression algorithm.

One trick that helps compressions is discretization: i.e. clumping together
observations taken over a continuous range :-) into a small number of
ranges. Humans often discretize real world data. For example, parents often
share tips for "toddlers"; i.e. humans found between the breaks of age=1 and
age=3. Many researchers report that discretization improves the performance of a
learner since it gives a learner a smaller space to reason about, with more
examples in each part of the space [Do95](refs.md#Do95),[Fa93](refs.md#Fa93).

There are some very simple discretization methods (e.g. divide the column at
breaks equal to _(max - min)/10_ but that suffers from so many odd cases
that I jsut do not use it. Instead, I use the top-down clustering methods
described below, plus some sanity tricks that have proved useful over the years.

But before all that...

## Dull Columns and Irrelevant Ranges

Suppose we are using discretization to find better ways to achieve some goal
(e.g. some class called "happiness")

In this case, two important events are when:

- Discretization fails to split a column  into ranges; e.g. because the column is
  pure noise or it is not associated with any target goal.  We will call such a
  column _dull_ since it means means that we were unable to find useful
  structure within a column.
       + Note that the opposite of dull is `sharp`.

- When a `Range` is _irrelevant_; i.e. it does not contain a majority of the
  goal we seek,
       + Note that the opposite of irrelevant is `relevant`. 

As shown below, by ignoring dull columnns and irrelevant ranges, seemingly
complex data sets can be summarised in just a few ranges. There are some deep
mathematically reasons for believing that this is actually the expected
case... see the [math of data](maths.md).

"""

def sharp(data,  **options):
  "Only returns something is discretization can split the column."
  for col in data.x.cols.values():
    if isa(col,Num):
      ranges = supervisedDiscretization(data, col.pos, **options)
      if len(ranges) > 1:
        yield col.pos, ranges

def relevant(data, goal, **options):
  "Only returns a range if it contains the goal."
  for pos,ranges in sharp(data, **options):
    for range1 in ranges:
      if range1.report.mode == goal:
        yield pos,range1

def supervisedDiscretization(data, pos, **options):
  """Supervised discretization divides a numeric column using the data distributions
     in the klass column."""
  return  ediv(data._rows, # ediv is a discretizer explained below
               xx= lambda z: z.x[pos],
               yy= lambda z: z.y[0],
               **options) 
"""
## Top-Down Bi-Clustering

All the following tricks us the same top-down bi-clustering approach:

- Sort the rows by some column
- Run down the sorted column looking for the _best_ place to break the column in two.
      - Where _best_ might mean many things, discussed below.
- Recurse into both breaks.

These tricks discretize numeric columns into a list of useful `Range`s. The most
important part of the following class is the `pretty` method that lets us show a
range as some region between some values.

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

## Discretizing,  Sanely

Note that all these tricks use four sanity tricks:

- Don't waste time resorting the numeric columns for every level of the recursion:
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
all the following code looks something like this:

   def divide(lst) :
     cut = None
     lhs, rhs = nothing, everything(lst)
     score    = some initial value
     for i,new  in enumerate(lst):
       lhs += new                      # lhs is a `Col` and supports `__iadd__`
       rhs -= new                      # rhs is a `Col` and supports `__isub__`
       # body of discretizer goes here
     return cut

Note the last line: if the body of the discretizer cannot find any interesting `cuts`,
then this function returns `None`.

As to what goes into the body of the discretizer, based on the above sanity tricks, that
body looks like the following:

       trivial = 1.05,
       small   = rhs.sd()*0.2,
       enough  = sqrt(len(lst)))

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

Note the last line: `cut` is only updated if all the `if` statements are passed.

One more trick, then we can look at the code:

- Sometimes, in the following, we work with _pairs_ of columns looking for
  breaks in column1 such that it most divides up the associated values in column2.
        - e.g. imagine two columns of data, one called "age" and another called "dead?"
        - Somewhere around age>120, all the associated "dead?" entries will be "True"
        - So me might propose one break of "age" at around 120.
- Hence, in the following, all the `divide` codes have accessors `xx` and `yy`
  telling it what column to break on (the `xx` ones) in order to have most
  effct on the  other column `yy`. 
- For the simple case, where we are just dividing a column without reflecting
  on any other column, we just set ``yy=xx`` (e.g. see `sddiv`, below).

XXX explain this is a greedy search but, heh, its fayyad iranni so chill
__________________________________________________________________________
## Configuration Options

"""

The.divs = o(attr    = 0,      # a label for the ranges
             cohen   = 0.2,    # 'small' means sd()*cohen
             trivial = 1.05,   # need at least a 5% improvement
             enough  = None,   # enough items for a bin. default=n**0.5
             small   = None,   # when are numbers too small?
             verbose = False,
             minSd   = True)   # for numeric columns

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
         minSd   = The.divs.minSd):  
  # ---------------------------------------------------
  def divide(lst, out=[], lvl=0, cut=None):
    xlhs, xrhs   = Num(get=xx), Num(lst, get=xx)
    ylhs, yrhs   = Num(get=yy), Num(lst, get=yy)
    score,score1 = yrhs.sd(),None
    n            = len(lst)
    report       = copy(yrhs)
    for i,new in enumerate(lst):
      if not isMissing(xx(new)):
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

XXX [Fayyad irrani](refs.bib#Fa93)

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
      if not isMissing(xx(new)):
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



"""


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
 
@demo
def _ediv2():
  """Divide a numeric column accroding to how well it seperates the symbols in a
     second  column of symbols. """
  rseed(1)
  lst0=list('abcd')
  lst = []
  for _ in xrange(1000):
    for i,x in enumerate(lst0):
      lst += [[i+0.5*r(), x]] # 'a' is around 0.5, 'd' is around 3.5
  for y in ediv( lst,
                xx=lambda z: z[0],
                yy=lambda z: z[1]):
    print(y)

"""

-----| _ediv2 |-----------------------
# Divide a numeric column accroding to how well it seperates the symbols in a
# second  column of symbols.

['attr: 0', 'id: 0', 'lo: 0.0', 'n: 999', 'report: ["counts: {\'a\': 999}", \'mode: a\', \'most: 999\', \'n: 999\']', 'score: 0.0', 'up: 0.5']
['attr: 0', 'id: 1', 'lo: 0.5', 'n: 998', 'report: ["counts: {\'a\': 1, \'b\': 997}", \'mode: b\', \'most: 997\', \'n: 998\']', 'score: 0.01', 'up: 1.5']
['attr: 0', 'id: 2', 'lo: 1.5', 'n: 1002', 'report: ["counts: {\'c\': 999, \'b\': 3}", \'mode: c\', \'most: 999\', \'n: 1002\']', 'score: 0.03', 'up: 2.5']
['attr: 0', 'id: 3', 'lo: 2.5', 'n: 1001', 'report: ["counts: {\'c\': 1, \'d\': 1000}", \'mode: d\', \'most: 1000\', \'n: 1001\']', 'score: 0.01', 'up: 3.5']


"""

@demo
def _ediv3():
  arff=Arff("data/jedit-4.1.arff", prep=tf)
  print( [pos for pos,_ in sharp(arff.tubs) ] )

"""

-----| _ediv3 |-----------------------
[0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19]


"""  

@demo
def _ediv4():
  "Like _ediv1, put only print ranges relevant for 'true'."
  arff=Arff("data/jedit-4.1.arff", prep=tf)
  relevants= [(range1.score,arff.attributes[pos],range1)
              for pos,range1 in relevant( arff.tubs ,"true") ]
  for one in sorted(relevants):
    print(one)

"""
-----| _ediv4 |-----------------------
# Like _ediv1, put only print ranges relevant for 'true'.

0.7553754125614288, 'lcom', ['attr: 0', 'id: 1', 'lo: 217', 'n: 23', 'report: ["counts: {\'true\': 18, \'false\': 5}", \'mode: true\', \'most: 18\', \'n: 23\']', 'score: 0.76', 'up: 13445'])
(0.8904916402194913, 'ce', ['attr: 0', 'id: 2', 'lo: 13', 'n: 39', 'report: ["counts: {\'false\': 12, \'true\': 27}", \'mode: true\', \'most: 27\', \'n: 39\']', 'score: 0.89', 'up: 60'])
(0.9121156307204276, 'wmc', ['attr: 0', 'id: 2', 'lo: 15', 'n: 55', 'report: ["counts: {\'false\': 18, \'true\': 37}", \'mode: true\', \'most: 37\', \'n: 55\']', 'score: 0.91', 'up: 413'])
(0.9559312637896479, 'cam', ['attr: 0', 'id: 0', 'lo: 0', 'n: 61', 'report: ["counts: {\'false\': 23, \'true\': 38}", \'mode: true\', \'most: 38\', \'n: 61\']', 'score: 0.96', 'up: 0.25'])
(0.9709505944546686, 'rfc', ['attr: 0', 'id: 1', 'lo: 40', 'n: 85', 'report: ["counts: {\'false\': 34, \'true\': 51}", \'mode: true\', \'most: 51\', \'n: 85\']', 'score: 0.97', 'up: 505'])
(0.9852281360342516, 'moa', ['attr: 0', 'id: 1', 'lo: 2', 'n: 63', 'report: ["counts: {\'false\': 27, \'true\': 36}", \'mode: true\', \'most: 36\', \'n: 63\']', 'score: 0.99', 'up: 17'])
(0.9988455359952018, 'loc', ['attr: 0', 'id: 1', 'lo: 316', 'n: 100', 'report: ["counts: {\'false\': 48, \'true\': 52}", \'mode: true\', \'most: 52\', \'n: 100\']', 'score: 1.0', 'up: 23590'])
(0.9996734260048917, 'ic', ['attr: 0', 'id: 1', 'lo: 2', 'n: 47', 'report: ["counts: {\'false\': 23, \'true\': 24}", \'mode: true\', \'most: 24\', \'n: 47\']', 'score: 1.0', 'up: 4'])
(1.0, 'max_cc', ['attr: 0', 'id: 2', 'lo: 6', 'n: 106', 'report: ["counts: {\'false\': 53, \'true\': 53}", \'mode: true\', \'most: 53\', \'n: 106\']', 'score: 1.0', 'up: 167'])

"""
@demo
def _ediv5():
  arff=Arff("data/jedit-4.1.arff", prep=tf)
  

  
if __name__ == "__main__":
  demos()
