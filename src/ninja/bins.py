from __future__ import division,print_function
import sys,os
sys.dont_write_bytecode=True


class o:
  def __init__(i, **entries):
    i.__dict__.update(entries)
  def __repr__(i):
    return str({k:v for k,v
                in i.__dict__.items()})

    
The=o(bins=o(cohen   = 0.3,
             enough  = None,
             minBins = 2,
             maxBins = 7,
             trivial = 1.05))

def isMissing(x): return x == "?"
def isSym(x): return isinstance(x,str)

  
def xx(z): return z.x
def yy(z): return z.y
def same(z): return z


class Col:
  def __add__(i,x):
    x=i.get(x)
    if not isMissing(x): i.add(x)
  def __repr__(i):
    return str(kv(i))
  
class Sym(Col):
  def __init__(i,inits=[],get=same):
    i.counts, i.most, i.mode, i.n = {},0,None,0
    i.get = get
    map(i.__add__,inits)
  def add(i,x):
    i.n += 1
    new = i,counts[x] = i.counts.get(x,0) + 1
    if new > t.most:
      i.most, i.mode = new,x

class Num(Col):
  def __init__(i,inits=[],get=same):
    i.mu,i.n,i.m2,i.up,i.lo = 0,0,0,-10e32,10e32
    i.get = get
    map(i.__add__,inits)
  def small(i,cohen=0.3): return i.sd()*cohen
  def wsd(i,n=1): return i.sd()*i.n/n
  def sd(i): return 0 if i.n <= 1 else (i.m2/(i.n - 1))**0.5
  def add(i,x):
    i.n += 1
    if x < i.lo: i.lo=x
    if x > i.up: i.up=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
  def __sub__(i,x):
    x = i.get(x)
    if not isMissing(x):
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/i.n
      i.m2 -= delta*(x - i.mu)

class Range:
  def __init__(i,attr=None,lo=None,up=None,has=None,score=None):
    i.attr,i.lo, i.up, i._has, i.score = attr,lo,up,has,score
  def __repr__(i):
    return str(kv(i))

def kv(i):
  return {k:v for k,v in i.__dict__.items() if k[0] != "_"}

def sdiv(lst,
         attr    = None,
         minBins = 2,
         maxBins = 16,
         cohen   = 0.3,
         trivial = 1.05,
         small   = None, 
         xx      = same,
         yy      = same):
  # --------------------------------
  def div(lst, out,lvl):
    cut        = None
    xlhs, xrhs = Num(get=xx), Num(lst, get=xx)
    ylhs, yrhs = Num(get=yy), Num(lst, get=yy)
    score      = yrhs.sd()
    n          = len(lst)
    old        = lst[0]
    for i,new in enumerate(lst):
      print(i,score,enough)
      xlhs + new
      xrhs - new
      ylhs + new
      yrhs - new
      print('.. '*lvl,"N",xrhs.n,xlhs.n)
      if xrhs.n < enough:
        break
      print(1)
      if xlhs.n >= enough:
        print('.. '*lvl,2,o(new=xx(new),old=xx(lst[0]),small=small,start=xx(lst[0])))
        if xx(new) - xx(lst[0]) > small:
          print('.. '*lvl,3)
          score1 = ylhs.wsd(n) + yrhs.wsd(n)
          if score1*trivial < score:
            print('!! '*lvl,4)
            cut,score = i,score1,
      old = new
      
    # --------------------------------
    if cut:
      div(lst[:cut], out,lvl+1)
      div(lst[cut:], out,lvl+1)
    else:
      out = out + [Range(attr=attr,     score=score,
                         lo=xx(lst[0]), up=xx(lst[-1]),
                         has=lst)]
    return out
  # --------------------------------
  if lst:
    small   = small or Num(lst,get=xx).small(cohen)
    maxBins = min(len(lst), minBins)
    few     = max(minBins, len(lst)/maxBins)
    enough  = int(len(lst)/few)
    return div( sorted(lst[:], key=xx), [] ,1) # copied, sorted
  else:
    return []
  
print sdiv([x for x in xrange(10)],small=3))
sys.exit()
         
class row:
  def __init__(i,x=None,y=None):
    i.x = x or []
    i.y = y or []
    
class tub:
  def __init__(i,get = same):
    i.rows=[]
    i.get = get
    i.abouts = {}
  def __add__(i,lst):
    lst = i.get(lst)
    for j,val in enumerate(lst):
      if not isMissing(val):
        about = i.about.get(j,None)
        if not about:
          about = i.about[j] = sym() if isSym(val) else num()
        about + val
        
class twintub:
  def __init__(i):
    i.x=tub(xx)
    i.y=tub(yy)
  def __add__(i,row):
    i.x + row
    i.y + row
  
    
