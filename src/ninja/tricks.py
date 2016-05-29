"""
# tricks.py  : Standard Python tricks

(C) 2016 tim@menzies.us, MIT license

___________________________________________________

## Header tricks

"""
from __future__ import division,print_function
import sys,random,re,copy,os,inspect
sys.dont_write_bytecode=True # don't write irritating .pyc files

"""___________________________________________________

## Generic container trick (fields, but no methods).
"""

class o:
  def __init__(i, **adds): i.__dict__.update(adds)
  def __repr__(i)        : return str(kv(i.__dict__))

"""___________________________________________________

## Meta tricks (one day, this will make sense)
"""

def same(z): return z

Demos = []
def demo(f):
  Demos.append(f); return f
def demos():
  for f in Demos:
    print("\n-----| %s |-----------------------" % f.__name__)
    if f.__doc__:
      print("# "+ re.sub(r'\n[ \t]*',"\n# ",f.__doc__)+"\n")
    f()
  
"""___________________________________________________

## Options trick
"""

# 'The' is the place to hold global options

The=o(tricks=o(round=2))

"""___________________________________________________

## Standard alias tricks
"""

rseed=random.seed
r=random.random
copy=copy.deepcopy

@demo
def _rand():
  rseed(1)
  print([r() for _ in range(5)])
  rseed(1)
  print([r() for _ in range(5)])
  
"""___________________________________________________

##  Dictionary tricks
"""

def kv(d, private="_",
       places=The.tricks.round):
  "Print dicts, keys sorted (ignoring 'private' keys"
  def _private(key):
    return key[0] == private
  def pretty(x):
    return round(x,places) if isa(x,float) else x
  return ['%s: %s' % (k,pretty(d[k]))
          for k in sorted(d.keys())
          if not _private(k)]

"""___________________________________________________

## Printing tricks
"""

def dot(x='.'):
  "Write without new line"
  sys.stdout.write(x)
  sys.stdout.flush()

"""___________________________________________________

## Type tricks
"""

def isa(x,y): return isinstance(x,y)
def isSym(x): return isa(x,str)

def thing(x):
  "Coerce to a float or an int or a string"
  try: return int(x)
  except ValueError:
    try: return float(x)
    except ValueError:
      return x

if __name__ == '__main__': demos()
