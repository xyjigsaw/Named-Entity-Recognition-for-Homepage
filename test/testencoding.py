#如果你的python没有安装chardet模块，你需要首先安装一下chardet判断编码的模块哦
#author:pythontab.com
import chardet
import urllib.request
#先获取网页内容
data1 = urllib.request.urlopen('http://staff.ustc.edu.cn/~qiliuql/').read()
#用chardet进行内容分析
chardit1 = chardet.detect(data1)

print(chardit1['encoding'])