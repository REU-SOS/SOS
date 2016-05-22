class o:
  def __init__(i, **entries):
    i.__dict__.update(entries)
  def __repr__(i):
    return str({k=v for k,v
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


class Sym:
  def __init__(i,inits=[]):
    i.counts, i.most, i.mode, i.n = {},0,None,0
    map(i.__add__,inits)
  def __add__(i,x):
    if not isMissing(x):
      i.n += 1
      new = i,counts[x] = i.counts.get(x,0) + 1
      if new > t.most:
        i.most, i.mode = new,x

class Num:
  def __init__(i,inits=[]):
    i.mu,i.n,i.m2,i.up,i.lo = 0,0,0,-10e32,10e32
    map(i.__add__,inits)
  def sd(i):
    return 0 if i.n <= 1 else (i.m2/(i.n - 1))**0.5
  def __add__(i,x):
    if not isMissing(x):
      i.n += 1
      if x < i.lo: i.lo=x
      if x > i.hi: i.hi=x
      delta = x - i.mu
      i.mu += delta/i.n
      i.m2 += delta*(x - i.mu)
  def __sub__(i,x):
    if not isMissing(x):
      i.n -= 1
      delta = x - i.mu
      i.mu -= delta/i.n
      i.m2 -= delta*(x - i.mu)

class Range:
  def __init__(i,attr=None,lo=None,hi=None,has=None):
    i.attr,i.lo, i.hi, i.has = attr,lo,hi,has

def sdiv(lst, attr=0,
         tiny=4, cohen=0.3, smally=0.01,smallx=0.001
         x      = lambda z: z.x[0],
         y      = lambda z: z.y[0]):
  "Divide lst of (x,y) using variance of y."
  #----------------------------------------------
  def divide(this): #Find best divide of 'this'
    lhs,rhs = Num(), Num(y(z) for z in this)
    n0, score, cut,mu = rhs.n, rhs.sd(), None,rhs.mu
    old = this[0]
    for j,one  in enumerate(this):
      if one - old > smallx:
        old = one
        if lhs.n > tiny and rhs.n > tiny:
          maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
          if maybe < score:
            if abs(lhs.mu - rhs.mu) >= smally:
              cut,score = j,maybe
      rhs - y(one)
      lhs + y(one)
    return cut,mu,score,this
  #----------------------------------------------
  def recurse(this, cuts):
    cut,mu,sd,part0 = divide(this)
    if cut:
      recurse(this[:cut], cuts)
      recurse(this[cut:], cuts)
    else:
      cuts += [Range(attr = attr,
                     x    = o(lo=x(this[0]), hi=x(this[-1])),
                     y    = o(mu=mu, sd=sd),
                     has  = this)]
    return cuts
  #---| main |-----------------------------------
  smally = smally or Num(y(z) for z in lst).sd()*cohen
  smallx = smallx or Num(x(z) for z in lst).sd()*cohen
  if lst:
    return recurse(sorted(lst,key=x), [] )

def ediv(lst, lvl=0,tiny=The.tree.min,
         dull=The.math.brink.cohen,
         num=lambda x:x[0], sym=lambda x:x[1]):
  "Divide lst of (numbers,symbols) using entropy."""
  #----------------------------------------------
  #print watch
  def divide(this,lvl): # Find best divide of 'this' lst.
    def ke(z): return z.k()*z.ent()
    lhs,rhs   = Sym(), Sym(sym(x) for x in this)
    n0,k0,e0,ke0= 1.0*rhs.n,rhs.k(),rhs.ent(),ke(rhs)
    cut, least  = None, e0
    last = num(this[0])
    for j,x  in enumerate(this): 
      rhs - sym(x); #nRhs - num(x)
      lhs + sym(x); #nLhs + num(x)
      now = num(x)
      if now != last:
        if lhs.n > tiny and rhs.n > tiny: 
          maybe= lhs.n/n0*lhs.ent()+ rhs.n/n0*rhs.ent()       
          if maybe < least : 
            gain = e0 - maybe
            delta= log2(3**k0-2)-(ke0- ke(rhs)-ke(lhs))
            if gain >= (log2(n0-1) + delta)/n0: 
              cut,least = j,maybe
      last= now
    return cut,least
  #--------------------------------------------
  def recurse(this, cuts):
    cut,e = divide(this)
    if cut: 
      recurse(this[:cut], cuts); 
      recurse(this[cut:], cuts)
    else:   
      lo    = num(this[0])
      hi    = num(this[-1])
      cuts += [o(at=lo, 
                 e=e,_has=this,
                 range=(lo,hi))]
  return recurse(this,cuts)

def ediv(lst, lvl=0,tiny=The.tree.min,
         dull=The.math.brink.cohen,
         num=lambda x:x[0], sym=lambda x:x[1]):
  "Divide lst of (numbers,symbols) using entropy."""
  #----------------------------------------------
  #print watch
  def divide(this,lvl): # Find best divide of 'this' lst.
    def ke(z): return z.k()*z.ent()
    lhs,rhs   = Sym(), Sym(sym(x) for x in this)
    n0,k0,e0,ke0= 1.0*rhs.n,rhs.k(),rhs.ent(),ke(rhs)
    cut, least  = None, e0
    last = num(this[0])
    for j,x  in enumerate(this):
      rhs - sym(x); #nRhs - num(x)
      lhs + sym(x); #nLhs + num(x)
      now = num(x)
      if now != last:
        if lhs.n > tiny and rhs.n > tiny:
          maybe= lhs.n/n0*lhs.ent()+ rhs.n/n0*rhs.ent()
          if maybe < least :
            gain = e0 - maybe
            delta= log2(3**k0-2)-(ke0- ke(rhs)-ke(lhs))
            if gain >= (log2(n0-1) + delta)/n0:
              cut,least = j,maybe
      last= now
    return cut,least
  #--------------------------------------------
  def recurse(this, cuts,lvl):
    cut,e = divide(this,lvl)
    if cut:
      recurse(this[:cut], cuts, lvl+1);
      recurse(this[cut:], cuts, lvl+1)
    else:
      lo    = num(this[0])
      hi    = num(this[-1])
      cuts += [Thing(at=lo,
                     e=e,_has=this,
                     range=(lo,hi))]

def chunks(l, n):
  n = max(1, n)
  return [l[i:i + n] for i in range(0, len(l), n)]

def bins(lst)
  lst = sorted(lst,key=xx)
  xlst = map(xx,lst)
  ylst = map(yy,lst)
  xcohen = Num(xlst) * cohen
  ycohen = Num(ylst) * cohen
  
  lst = chunks(lst,16)
  doomed={}
  old = lst[0]
  for j,one in enumerate(lst):
    if xx(one[-1]) - xx(one[0]) < xcohen or
       yy(one[-1]) - yy(one[0]) < ycohen or
       cliffsDelta(
         
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
  
    
