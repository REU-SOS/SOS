from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True

from ranges import *

def tf(line):
  klass=line[-1]
  if isinstance(klass,(int,float)):
    line[-1]  = 'true' if klass > 0 else 'false'
  return line
  
def muPrune(a,cohen=0.3):
  for n,col in enumerate(a.tubs.x.cols.values()):
    if isinstance(col,Num):
      rs = mudiv(a.tubs._rows,attr=a.attributes[n],cohen=cohen,
                xx=lambda z:z[n])
      if len(rs) > 1: # ignore columns that never divide
        for r in rs:
            yield r

def _muPrune(f,cohen=0.3):
  a=Arff(f,filter=tf)
  print("-" * 10)
  for r in muPrune(a,cohen=cohen):
    print(r.attr,r.pretty(), r.report,r.score)


def xPrune(a,cohen=0.3,f=sddiv):
  for n,col in enumerate(a.tubs.x.cols.values()):
    if isinstance(col,Num):
      rs = f(a.tubs._rows,attr=a.attributes[n],cohen=cohen,
                xx=lambda z:z[n])
      if len(rs) > 1: # ignore columns that never divide
        for r in rs:
            yield r

def _sdPrune(f,cohen=0.3):
  a=Arff(f,filter=tf)
  print("-" * 10)
  old = None
  for r in xPrune(a,cohen=cohen):
    if r.attr != old:
      print("----")
      old =r.attr
    print(r.attr,r.pretty(), r.report,r.score)

def _cohenPrune(f,cohen=0.3):
  a=Arff(f,filter=tf)
  print("-" * 10)
  old = None
  for r in xPrune(a,cohen=cohen,f=cohenPrune):
    if r.attr != old:
      print("----")
      old =r.attr
    print(r.attr,r.pretty(), r.report,r.score)
    

def ePrune(a,goal):
  """return ranges within a's numeric columns 
     that support at least one split and
     whose mode is goal"""
  for n,col in enumerate(a.tubs.x.cols.values()):
    if isinstance(col,Num):
      rs = ediv(a.tubs._rows,attr=a.attributes[n])
      if len(rs) > 1: # ignore columns that never divide
        for r in rs:
          if r.report.mode == goal:
            yield r
                           
def _ePrune(f,goal):
  """For each range whose mode is goal"""
  a=Arff(f,filter=tf)
  print("-" * 10)
  for r in sorted(ePrune(a,goal),
                  key=lambda z:z.score):
    print(r.attr,r.pretty(), r.report,r.score)
    
    #print(r.attr,r,pretty,r.report)
    
  
if __name__ == "__main__":
  #_sdiv()
  #print("")
  #_ediv()
  
  #_muPrune("data/jedit-4.1.arff", cohen=0.3)
  #_cohenPrune("data/jedit-4.1.arff", cohen=0.3)
  #_sdPrune("data/jedit-4.1.arff", cohen=0.3)
  _ePrune("data/jedit-4.1.arff","true")
  
  #fewAreCalled("data/jedit-4.1.arff","true")
  #fewAreCalled("data/ivy-1.1.arff","true")
  #fewAreCalled("data/diabetes.arff","tested_positive")
 
