#!/user/bin/env python
#!encoding=utf-8
from Common.ExcelTools.ExcelCreateReport import ExcelCreateReport

'''执行全套excel测试用例并生成ExcelReport报告'''

createexcel=ExcelCreateReport()
createexcel.create_report('车之联api接口测试报告')

