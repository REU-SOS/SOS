from __future__ import division,print_function
import sys,os,random,math,re
sys.dont_write_bytecode=True

import cProfile
rseed=random.seed
r=random.random

class o:
  def __init__(i, **entries):
    i.__dict__.update(entries)
  def __repr__(i):
    return str({k:v for k,v
                in i.__dict__.items()})
 
The=o(bins=o(attr    = 0,      # a label for the ranges
             cohen   = 0.2,    # 'small' means sd()*cohen
             trivial = 1.05,   # need at least a 5% improvement
             enough  = None,   # enough items for a bin. default=n**0.5
             small   = None,   # when are numbers too small?
             verbose = False))
             
def isMissing(x): return x == "?"
def isSym(x): return isinstance(x,str)
  
def xx(z): return z.x
def yy(z): return z.y
def same(z): return z

def thing(x):
  try: return int(x)
  except ValueError:
    try: return float(x)
    except ValueError:
      return x
          
class Col:
  def __init__(i,inits=[],get=same):
    i.reset()
    i.get = get
    map(i.__add__,inits)
  def __add__(i,x):
    x = i.get(x)
    if not isMissing(x): i.add(x)
  def __sub__(i,x):
    x = i.get(x)
    if not isMissing(x): i.sub(x)
  def __repr__(i):
    return str(kv(i))
  
class Sym(Col):
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
    tmp = 0
    for val in i.counts.values():
      p = val/i.n
      if p:
        tmp -= p*math.log(p,2)
    return tmp
      
class Num(Col):
  def reset(i):
    i.mu,i.n,i.m2,i.up,i.lo = 0,0,0,-10e32,10e32
  def small(i,cohen=0.3):
    return i.sd()*cohen
  def sd(i):
    return 0 if i.n <= 1 else (i.m2/(i.n - 1))**0.5
  def add(i,x):
    i.n += 1
    if x < i.lo: i.lo=x
    if x > i.up: i.up=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    i.n  -= 1
    delta = x - i.mu
    i.mu -= delta/i.n
    i.m2 -= delta*(x - i.mu)
      
class Range:
  def __init__(i, attr=None, n=None, lo=None,
               id=None, up=None, has=None, score=None):
    i.attr, i.lo, i.up, i._has = attr, lo, up, has
    i.score, i.n, i.id         = score, n, id
  def __repr__(i):
    return str(kv(i))

def kv(i):
  return {k:v for k,v in i.__dict__.items() if k[0] != "_"}

def sdiv(lst,
         attr    = The.bins.attr,     # a label for the ranges
         cohen   = The.bins.cohen,    # 'small' means sd()*cohen
         trivial = The.bins.trivial,  # need at least a 5% improvement
         enough  = The.bins.enough,   # enough items for a bin. default=n**0.5
         small   = The.bins.small,    # when are numbers too small?
         verbose = The.bins.verbose,  # prints some trace info
         xx      = same,   # access independent variable
         yy      = same):  # access dependent   variable
  # ---------------------------------------------------
  def divide(lst, out=[], lvl=0, arg=None):
    xlhs, xrhs   = Num(get=xx), Num(lst, get=xx)
    ylhs, yrhs   = Num(get=yy), Num(lst, get=yy)
    score,score1 = yrhs.sd(),None
    n            = len(lst)
    for i,new in enumerate(lst):
      xlhs + new; xrhs - new
      ylhs + new; yrhs - new
      if xrhs.n < enough:
        break
      else:
        if xlhs.n >= enough:
          start, here, stop = xx(lst[0]), xx(new), xx(lst[-1])
          if here - start > small:
            if stop - here > small:
              score1 = ylhs.n/n*ylhs.sd() + yrhs.n/n*yrhs.sd()
              if score1*trivial < score:
                arg,score = i,score1
    # --- end for loop -------------------------------
    if verbose:
      print('.. '*lvl,len(lst),score1 or '.')
    if arg:
      divide(lst[:arg], out= out, lvl= lvl+1)
      divide(lst[arg:], out= out, lvl= lvl+1)
    else:
      out.append(Range(attr=attr, score=score,
                       n=len(lst), id=len(out),
                       lo=xx(lst[0]), up=xx(lst[-1]),
                       has=lst))
    return out
  # --- end function div -----------------------------
  if not lst: return []
  small  = small  or Num(lst,get=xx).small(cohen)
  enough = enough or len(lst)**0.5
  return divide( sorted(lst[:], key=xx), out=[] ,lvl=0) # copied, sorted

def ediv(lst,
         attr    = The.bins.attr,
         cohen   = The.bins.cohen,
         trivial = The.bins.trivial,
         enough  = The.bins.enough,
         small   = The.bins.small,
         verbose = The.bins.verbose,
         xx      = lambda z:z[0],
         yy      = lambda z:z[-1]):
  def divide(lst, out=[], lvl=0, arg=None):
    def ke(z): return z.k()*z.ent()
    arg            = None
    xlhs, xrhs     = Num(get=xx), Num(lst, get=xx)
    ylhs, yrhs     = Sym(get=yy), Sym(lst, get=yy)
    k0, e0, ke0    = yrhs.k(), yrhs.ent(), ke(yrhs)
    score,score1   = yrhs.ent(),None
    n = len(lst)
    for i,new  in enumerate(lst):
      xlhs + new; xrhs - new
      ylhs + new; yrhs - new
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
                  arg,score = i,score1
  #----------------------------------------------
    if verbose:
      print('.. '*lvl,len(lst),score1 or '.')
    if arg:
      divide(lst[:arg], out=out, lvl=lvl+1)
      divide(lst[arg:], out=out, lvl=lvl+1)
    else:
      out.append(Range(attr=attr, score=score,
                       n=len(lst), id=len(out),
                       lo=xx(lst[0]), up=xx(lst[-1]),
                       has=lst))                       
    return out
  #---| main |-----------------------------------
  if not lst: return []
  small  = small  or Num(lst,get=xx).small(cohen)
  enough = enough or len(lst)**0.5
  return divide(sorted(lst,key=xx), out=[], lvl=0)
  
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
      lst2 += [[i+0.5*r(), x]]
  lst2 = sorted(lst2)
  for y in ediv(lst2):
    print(y)
         
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
        about = i.abouts.get(j,None)
        if not about:
          about = i.abouts[j] = Sym() if isSym(val) else Num()
        about + val
        
class twintub:
  def __init__(i,xx=xx,yy=yy):
    i.x=tub(xx)
    i.y=tub(yy)
    i._rows = []
  def __add__(i,row):
    i.x + row
    i.y + row
    i._rows += [row]

class arff:
  def __init__(i, f):
    i.tubs    = twintub(xx=lambda z: z[:-1],
                       yy=lambda z: z[-1])
    i.bad    = r'(["\'\r\n]|#.*)'
    i._header = []
    i.read(f)
  def atData(i,x):
    return re.match(r'^[ \t]*@DATA',
                    x,re.IGNORECASE)
  def header(i):
    return "\n".join(i._header)
  def read(i,f):
    pre    = True
    with open(f)  as fs:
      for line in fs:
        line = re.sub(i.bad, "", line)
        if pre:
          i._header += [line]
        if i.atData(line):
          pre    = False
        elif not pre:
          i.tubs + map(thing, line.split(","))
  
if __name__ == "__main__":
  #_sdiv()
  #print("")
  #_ediv()
  a=arff("data/jedit-4.1.arff")
  print(a.header())

