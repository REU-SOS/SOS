from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True

"""

e.g.
NINJA> python3 abcd.py
sdsa ada
a b
a a
a c
a d
b a
# db                   rx            n    a    b   c   d    acc pd  pf  prec f   g class
----------------------------------------------------------------------------------------
# sdsa                 ada           1    3    1   1    0   20   0  25   0   0   0 b
# sdsa                 ada           0    4    0   1    0   20   0  20   0   0   0 d
# sdsa                 ada           4    0    3   1    1   20  25 100  50  33   0 a
# sdsa                 ada           0    4    0   1    0   20  25  20   0   0  38 c
"""
 
def demo():
  log=None
  for line in sys.stdin:
    one, two = line.split()
    if log:
      log(one, two)
    else:
      actual, predicted = one, two
      log = Abcd( actual, predicted )
  log.report()

class o:
  def __init__(i,**d) : i.add(**d)
  def has(i): return i.__dict__
  def add(i,**d) : i.has().update(**d); return i
  def __setitem__(i,k,v): i.has()[k] = v
  def __getitem__(i,k)  : return i.has()[k]
  def __repr__(i) :
    f = lambda z: z.__class__.__name__ == 'function'
    name = lambda z: z.__name__ if f(z) else z
    public = lambda z: not "_" is z[0]
    d    = i.has()
    show = [':%s=%s' % (k,name(d[k])) 
            for k in sorted(d.keys()) if public(k)]
    return '{'+' '.join(show)+'}'
    
class Abcd: 
  def __init__(i,db="all",rx="all"):
    i.db = db; i.rx=rx;
    i.yes = i.no = 0
    i.known = {}; i.a= {}; i.b= {}; i.c= {}; i.d={}
  def __call__(i,actual=None,predict=None):
    i.knowns(actual)
    i.knowns(predict)
    if actual == predict: i.yes += 1 
    else                :  i.no += 1
    for x in  i.known:
      if actual == x:
        if  predict == actual: i.d[x] += 1 
        else                 : i.b[x] += 1
      else:
        if  predict == x     : i.c[x] += 1 
        else                 : i.a[x] += 1
  def knowns(i,x):
    if not x in i.known:
      i.known[x]= i.a[x]= i.b[x]= i.c[x]=i.d[x]=0.0
    i.known[x] += 1
    if (i.known[x] == 1):
      i.a[x] = i.yes + i.no
  def header(i):
    print("#",
        ('{0:20s} {1:11s}   {2:4s} {3:4s} {4:4s}'+\
        '{5:4s}{6:4s} {7:3s} {8:3s} {9:3s} '+ \
        '{10:3s} {11:3s}{12:3s}{13:10s}').format( 
        "db","rx","n","a","b","c","d","acc","pd",
        "pf","prec","f","g","class"))
    print('-'*100)
  def scores(i):
    def p(y) : return int(100*y + 0.5)
    def n(y) : return int(y)
    pd  = pf = pn = prec = g = f = acc = 0
    out = {}
    for x in i.known:
      a= i.a[x]; b= i.b[x]; c= i.c[x]; d= i.d[x]
      if (b+d)    : pd   = d     / (b+d)
      if (a+c)    : pf   = c     / (a+c)
      if (a+c)    : pn   = (b+d) / (a+c)
      if (c+d)    : prec = d     / (c+d)
      if (1-pf+pd): g    = 2*(1-pf)*pd / (1-pf+pd)
      if (prec+pd): f    = 2*prec*pd/(prec+pd)
      if (i.yes + i.no): acc= i.yes/(i.yes+i.no)
      out[x] = o(db=i.db, rx=i.rx, yes= n(b+d),
                 all=n(a+b+c+d), a=n(a),
                 b=n(b), c=n(c), d=n(d), acc=p(acc), pd=p(pd),
                 pf=p(pf), prec=p(prec), f=p(f), g=p(g),x=x)
    return out
  def report(i):
    i.header()
    for x,s in sorted(i.scores().items()):
      print("#",
       ('{0:20s} {1:10s} {2:4d} {3:4d} {4:4d}'+\
        '{5:4d} {6:4d} {7:4d} {8:3d} {9:3d} '+ \
        '{10:3d} {11:3d} {12:3d} {13:10s}').format(
          s.db, s.rx,  s.yes, s.a, s.b, s.c, s.d, 
          s.acc, s.pd, s.pf, s.prec, s.f, s.g, x))
   
if __name__ == "__main__":
  demo()
