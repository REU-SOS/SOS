from __future__ import division,print_function
import sys,os,random,math,re,copy
sys.dont_write_bytecode=True

import cProfile
rseed=random.seed
r=random.random
copy=copy.deepcopy

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
    i._get = get
    map(i.__add__,inits)
  def __add__(i,x):
    x = i._get(x)
    if not isMissing(x): i.add(x)
  def __sub__(i,x):
    x = i._get(x)
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
  def __init__(i, attr=None, n=None, lo=None,report=None,
               id=None, up=None, has=None, score=None):
    i.attr, i.lo, i.up, i._has = attr, lo, up, has
    i.score, i.n, i.id         = score, n, id
    i.report=report
  def __repr__(i):
    return str(kv(i))
  def pretty(i):
    return '[%s..%s]' % (i.lo,i.up)

def kv(i):
  keys = sorted(i.__dict__.keys())
  return ['%s: %s' % (k,i.__dict__[k]) for k in keys if k[0] != "_"]

def mudiv(lst,
         attr    = The.bins.attr,
         cohen   = The.bins.cohen,
         trivial = The.bins.trivial,
         enough  = The.bins.enough,
         small   = The.bins.small,
         verbose = The.bins.verbose,
         xx      = lambda z:z[0]):
  def divide(lst, out=[], lvl=0, arg=None):
    arg       = None
    lhs, rhs  = Num(get=xx), Num(lst, get=xx)
    mu,mu1    = rhs.mu,None
    report    = copy(rhs)
    n = len(lst)
    for i,new  in enumerate(lst):
      lhs + new; rhs - new
      lhs + new; rhs - new
      if rhs.n < enough:
        break
      else:
        if lhs.n >= enough:
          start, here, stop = xx(lst[0]), xx(new), xx(lst[-1])
          if here - start > small:
            if stop - here > small:
              mu1 = lhs.n/n*(mu - lhs.mu)**2 + rhs.n/n*(mu - rhs.mu)**2
              if mu1*trivial < mu:
                arg,mu = i,mu1
  #----------------------------------------------
    if verbose:
      print('.. '*lvl,len(lst),score1 or '.')
    if arg:
      divide(lst[:arg], out=out, lvl=lvl+1)
      divide(lst[arg:], out=out, lvl=lvl+1)
    else:
      out.append(Range(attr=attr, score=mu, report=report,
                       n=len(lst), id=len(out),
                       lo=xx(lst[0]), up=xx(lst[-1]),
                       has=lst))                       
    return out
  #---| main |-----------------------------------
  if not lst: return []
  small  = small  or Num(lst,get=xx).small(cohen)
  enough = enough or len(lst)**0.5
  return divide(sorted(lst,key=xx), out=[], lvl=0)

def _mudiv():
  rseed(1)
  n   = 1000
  lst = [r()**2 for x in xrange(n)]
  lst = lst + [r()**0.5 for x in xrange(n)]
  for y in mudiv(lst,xx=same,cohen=0.3):
    print(y)

def sddiv(lst,**d):
  d['yy'] = d['xx']
  return sdiv(lst,**d)

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
    report       = copy(yrhs)
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
    report         = copy(yrhs)
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
    i._get = get
    i.abouts = {}
  def __add__(i,lst):
    lst = i._get(lst)
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
  def __init__(i, f, filter=same):
    i.tubs = twintub(xx=lambda z: z[:-1],
                     yy=lambda z: z[-1:])
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
        if line and not i.empty(line):
          if data:
            line = line.split(",")
            line = i.filter(map(thing,line))
            i.tubs + line
          else:
            line = line.split()
            if i.at(line[0],'RELATION'):
              i.relation = line[1]
            elif i.at(line[0],'ATTRIBUTE'):
              i.attributes += [line[1]]
            elif i.at(line[0],'DATA'):
              data=True

def tf(line):
  klass=line[-1]
  if isinstance(klass,(int,float)):
    line[-1]  = 'true' if klass > 0 else 'false'
  return line
  
def muPrune(a,cohen=0.3):
  for n,about in enumerate(a.tubs.x.abouts.values()):
    if isinstance(about,Num):
      rs = mudiv(a.tubs._rows,attr=a.attributes[n],cohen=cohen,
                xx=lambda z:z[n])
      if len(rs) > 1: # ignore columns that never divide
        for r in rs:
            yield r

def _muPrune(f,cohen=0.3):
  a=arff(f,filter=tf)
  print("-" * 10)
  for r in muPrune(a,cohen=cohen):
    print(r.attr,r.pretty(), r.report,r.score)


def sdPrune(a,cohen=0.3):
  for n,about in enumerate(a.tubs.x.abouts.values()):
    if isinstance(about,Num):
      rs = sddiv(a.tubs._rows,attr=a.attributes[n],cohen=cohen,
                xx=lambda z:z[n])
      if len(rs) > 1: # ignore columns that never divide
        for r in rs:
            yield r

def _sdPrune(f,cohen=0.3):
  a=arff(f,filter=tf)
  print("-" * 10)
  for r in sdPrune(a,cohen=cohen):
    print(r.attr,r.pretty(), r.report,r.score)
    

def interesting(a,goal):
  """return ranges within a's numeric columns 
     that support at least one split and
     whose mode is goal"""
  for n,about in enumerate(a.tubs.x.abouts.values()):
    if isinstance(about,Num):
      rs = ediv(a.tubs._rows,attr=a.attributes[n],
                    xx=lambda z:z[n],
                    yy= lambda z:z[-1])
      if len(rs) > 1: # ignore columns that never divide
        for r in rs:
          if r.report.mode == goal:
            yield r
                           
def fewAreCalled(f,goal):
  """For each range whose mode is goal"""
  a=arff(f,filter=tf)
  print("-" * 10)
  for r in sorted(interesting(a,goal),
                  key=lambda z:z.score):
    print(r.attr,r.pretty(), r.report,r.score)
    
    #print(r.attr,r,pretty,r.report)
    
  
if __name__ == "__main__":
  #_sdiv()
  #print("")
  #_ediv()
  
  _muPrune("data/jedit-4.1.arff", cohen=0.3)
  _sdPrune("data/jedit-4.1.arff", cohen=0.3)
  
  #fewAreCalled("data/jedit-4.1.arff","true")
  #fewAreCalled("data/ivy-1.1.arff","true")
  #fewAreCalled("data/diabetes.arff","tested_positive")
 

