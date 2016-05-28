from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True

from tubs import *

The.divs = o(attr    = 0,      # a label for the ranges
             cohen   = 0.2,    # 'small' means sd()*cohen
             trivial = 1.05,   # need at least a 5% improvement
             enough  = None,   # enough items for a bin. default=n**0.5
             small   = None,   # when are numbers too small?
             verbose = False)

def mudiv(lst,
         attr    = The.divs.attr,
         cohen   = The.divs.cohen,
         trivial = The.divs.trivial,
         enough  = The.divs.enough,
         small   = The.divs.small,
         verbose = The.divs.verbose,
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
  return sdiv(lst,
              yy=d['xx'],
              **d)

def cohenPrune(lst,**d):
  return sddiv(lst,
              minSd=False,
              **d)

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
              if minSd:
                score1 = ylhs.n/n*ylhs.sd() + yrhs.n/n*yrhs.sd()
                if score1*trivial < score:
                  arg,score = i,score1
              else:
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
         attr    = The.divs.attr,
         cohen   = The.divs.cohen,
         trivial = The.divs.trivial,
         enough  = The.divs.enough,
         small   = The.divs.small,
         verbose = The.divs.verbose,
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
         
