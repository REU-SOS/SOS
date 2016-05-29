from __future__ import print_function

import re,os,sys
d=dict(
_UNDER400="""
<center><img width=400 src="https://www.lahc.edu/pageunderconstruction.png"></center>
"""
)

print(re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
      .sub(lambda x: d[x.group()], sys.stdin.read()))
