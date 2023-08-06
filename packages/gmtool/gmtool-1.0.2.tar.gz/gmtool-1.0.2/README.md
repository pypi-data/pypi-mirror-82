#GM's little generation tool !

##1.Description
Generate sentence according to Regex Expression. Now only support signs like "{}()|".

##2.Tutorial
Example：
```angular2
from gmtool.re_generation import ReParse
regex='{你|我}好'
print(ReParse(regex).Parse())
```
Result：
```angular2
['好', '你好', '我好']
```