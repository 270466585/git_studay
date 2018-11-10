#!/user/bin/env python
#!encoding=utf-8
import re

set_strint='The sum of 7 and 9 is [7+9]'

pat=re.compile(r'\[(.+?)\]')
s=re.search(pat,set_strint)
num=eval(s.group(1))
result=re.sub(pat,str(num),set_strint)
print(result)
print(result)
