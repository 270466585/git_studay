#!/user/bin/env python
#!encoding=utf-8
import os

'''路径管理'''

#根目录
root_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__))).replace('\\','/')

#Data路径
data_path=os.path.join(root_path,'Data/').replace('\\','/')

#yaml文件路径
yaml_path=os.path.join(data_path,'url.yaml')

#Log路径
log_path=os.path.join(root_path,'Log/').replace('\\','/')

#Report路径
report_path=os.path.join(root_path,'Report/').replace('\\','/')

#Report目录下Excel路径
execlreport_path=os.path.join(report_path,'ExcelReport/').replace('\\','/')

#Report目录下Html路径
htmlreport_path=os.path.join(report_path,'HtmlReport/').replace('\\','/')

#config配置文件路径
config_path=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')+'/config.ini'

#TestCase用例路径
testcase_path=os.path.join(root_path,'TestCases/').replace('\\','/')
