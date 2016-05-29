"""

# arff.py : tricks for reading and writing an arff file

(C) 2016 tim@menzies.us, MIT license

"""

from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True
from tubs import *
Demos=[]


"""_______________________________________________________________________

This code reads a data file of the following form:

    @RELATION iris
    
    @ATTRIBUTE sepallength  NUMERIC
    @ATTRIBUTE sepalwidth   NUMERIC
    @ATTRIBUTE class        {Iris-setosa,Iris-versicolor,Iris-virginica}
  
    @DATA
    5.1,3.5,Iris-setosa
    4.9,3.0,Iris-setosa
    4.7,3.2,Iris-setosa
    ...

The `rows` after `@data` are stored in `Tubs` (where it is assumed the last
cell in each row is the class).  Other information is stored in a list of
`attributes` and the name of the `relation`.

The input rows from a file are all strings so first they are coerced to floats,
ints, or strings using `thing`.  Next, the coerced row is sent through a
customisable `prep` (which defaults to `same`).

Note that when reading the @XXX tags, `Arff` uses a case-insensitive match
(see the use of `re.IGNORECASE`, below).

"""
class Arff:
  def __init__(i, f, prep=same):
    i.tubs = Tubs()
    i.attributes = []
    i.relation   = 'relation'
    i.prep       = prep
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
        if line:
          if not i.empty(line): # skip blank lines
            if data:
              line = line.split(",")
              line = map(thing,line)
              indep= line[:-1]
              dep  = [line[-1]]
              row = i.prep(Row(x=indep,y=dep))
              i.tubs += row
            else:
              line = line.split()
              if i.at(line[0],'RELATION'):
                i.relation = line[1]
              elif i.at(line[0],'ATTRIBUTE'):
                i.attributes += [line[1]]
              elif i.at(line[0],'DATA'):
                data=True
  def write(i):
    lines=[]
    lines += ["@relation "+i.relation + "\n"]
    for pos,attr in enumerate(i.attributes):
      col = i.tubs.col(pos)
      txt=""
      if isa(col,Num):
        txt = "real"
      else:
        vals = set([i.tubs.cell(row,pos) for row in i.tubs._rows]) 
        txt = "{ " + ', '.join(vals)+ " }"
      lines += [ "@attribute "+attr+ " " + txt ]
    lines += ["\n@data\n"]
    for row in i.tubs._rows:
      lines += [ ', '.join(map(str,row.x + row.y)) ]
    return lines
    
"""_______________________________________________________________________
## demo

For example, consider the file `weather.arff`:

    @relation weather
    @attribute outlook     {sunny,  overcast, rainy}
    @attribute temperature real
    @attribute humidity    real
    @attribute windy       {TRUE , FALSE}
    @attribute play        {yes  , no}
    @data
    sunny,       85,         85,       FALSE,  no
    sunny,       80,         90,       TRUE,   no
    overcast,    83,         86,       FALSE,  yes
    rainy,       70,         96,       FALSE,  yes
    rainy,       68,         80,       FALSE,  yes
    rainy,       65,         70,       TRUE,   no
    overcast,    64,         65,       TRUE,   yes
    sunny,       72,         95,       FALSE,  no
    sunny,       69,         70,       FALSE,  yes
    rainy,       75,         80,       FALSE,  yes
    sunny,       75,         70,       TRUE,   yes
    overcast,    72,         90,       TRUE,   yes
    overcast,    81,         75,       FALSE,  yes
    rainy,       71,         91,       TRUE,   no

"""


def tf(row):
  klass=row.y[0]
  if isinstance(klass,(int,float)):
    row.y[0] = 'true' if klass > 0 else 'false'
  return row


@demo
def _arff():
  """If we read this file and print the headers on the _x_ tub, we see the
     distributions of symbols and numbers in the independent (non-class)
     columns."""
  a=Arff('data/weather.arff')
  for x in a.tubs.x.cols.items():
    print(x)

"""
{0: ["counts: {'rainy': 5, 'overcast': 4, 'sunny': 5}", 'mode: sunny', 'most: 5', 'n: 14'], 
 1: ['lo: 64', 'm2: 561.43', 'mu: 73.57', 'n: 14', 'up: 85'], 
 2: ['lo: 65', 'm2: 1375.21', 'mu: 81.64', 'n: 14', 'up: 96'], 
 3: ["counts: {'TRUE': 6, 'FALSE': 8}", 'mode: FALSE', 'most: 8', 'n: 14']}
}

"""

@demo
def _arffWrite():
  """If we read this file and print the headers on the _x_ tub, we see the
     distributions of symbols and numbers in the independent (non-class)
     columns."""
  a=Arff('data/weather.arff')
  print('\n'.join(a.write()))
    
if __name__ == '__main__': demos()


