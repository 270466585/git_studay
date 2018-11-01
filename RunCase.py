#!/user/bin/env python
#!encoding=utf-8
from Common.CommonTools.RunTools import RunTools

'''执行用例并生成测试报告、发送邮件'''

'''=======================HTMLTestReport测试报告======================='''
# runcase=RunTools()
# # suite=runcase.chooseDirCases('XTPZ_Cases','test*.py')   #加载测试用例
# suite=runcase.chooseAllCases('test*.py')
# # runcase.createHtmlReport('接口自动化测试--罗泽霖','接口自动化测试--罗泽霖',suite)   #执行用例并生成测试报告
# lastfile=runcase.get_last_HtmlReport()      #查找最新的测试报告
# runcase.sendEmail('接口自动化测试--罗泽霖',lastfile)      #发送邮件不带附件

'''=======================BeautifulReport测试报告======================='''
runcase=RunTools()
suite = runcase.chooseAllCases('test*.py')
runcase.createBeautifulReport('车之联接口自动化测试',suite)
lastfile=runcase.get_last_HtmlReport()                           #查找最新的测试报告
runcase._sendEmailWithFile('车之联接口自动化测试报告',lastfile)      #发送邮件带附件