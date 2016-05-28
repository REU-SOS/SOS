from __future__ import division,print_function
import sys,math
sys.dont_write_bytecode=True

from lib import *

def isMissing(x): return x == "?"
def xx(z): return z.x
def yy(z): return z.y
          
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
    return str(kv(i.__dict__))
  
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
    return 0 if i.n <= 2 else (i.m2/(i.n - 1))**0.5
  def add(i,x):
    i.n += 1
    if x < i.lo: i.lo=x
    if x > i.up: i.up=x
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    i.n   = max(0,i.n - 1)
    delta = x - i.mu
    i.mu  = max(0,i.mu - delta/i.n)
    i.m2  = max(0,i.m2 - delta*(x - i.mu))
      
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




class Row:
  def __init__(i,x=None,y=None):
    i.x = x or []
    i.y = y or []
    
class Tub:
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
        
class TwinTub:
  def __init__(i,xx=xx,yy=yy):
    i.x=Tub(xx)
    i.y=Tub(yy)
    i._rows = []
  def __add__(i,row):
    i.x + row
    i.y + row
    i._rows += [row]

class arff:
  def __init__(i, f, filter=same):
    i.tubs = TwinTub(xx=lambda z: z[:-1],
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


