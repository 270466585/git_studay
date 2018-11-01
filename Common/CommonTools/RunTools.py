#!/user/bin/env python
#!encoding=utf-8
import smtplib
import time
import unittest
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Common.CommonTools.HTMLTestRunner import HTMLTestRunner
from Common.CommonTools.PathTools import *
from Common.CommonTools.ConfigReadTools import ConfigReadTools
from BeautifulReport import BeautifulReport

'''运行用例、生成报告、发送邮件相关函数封装'''

#读取配置文件信息
configread=ConfigReadTools(config_path)
emailconf=configread.get_section_item('EMAIL_CONF')

class RunTools:
    def sendEmail(self,subject,emailfile):
        '''
        发送邮件（包括发送文本邮件、发送带附件邮件）
        :param subject: 邮件主题
        :param emailfile: email文件
        '''
        self._sendEmail(subject,emailfile)
        self._sendEmailWithFile(subject,emailfile)

    def _sendEmail(self, subject, emailfile):
        '''
        发送邮件不带附件
        :param subject:邮件主题
        :param email: 邮件文件
        '''
        # 读取邮件内容
        with open(emailfile, 'rb') as fp:
            mail_body = fp.read()

        # 指定发送方与接收方
        sender = emailconf['Email_sender']
        receiver = emailconf['Email_receiver']

        # 配置邮件相关参数
        msg = MIMEText(mail_body, 'html', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = sender
        msg['To'] = receiver

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(emailconf['Smtp_connect'])
        smtp.login(emailconf['Smtp_username'], emailconf['Smtp_password'])
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()

    def _sendEmailWithFile(self, subject, emailfile):
        '''
        发送邮件带附件
        :param subject:发送邮件主题
        :param emailfile: 邮件文件
        '''
        # 读取邮件
        with open(emailfile, 'rb') as fp:
            emailread = fp.read()

        # 指定发送方与接收方
        sender = emailconf['Email_sender']
        receiver = emailconf['Email_receiver']

        # 加载邮件附件
        att = MIMEText(emailread, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment;filename=%s' % self.lastfile

        # 配置邮件信息
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = Header(subject, "utf-8")
        msgRoot['From'] = sender
        msgRoot['To'] = receiver
        msgRoot.attach(att)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(emailconf['Smtp_connect'])
        smtp.login(emailconf['Smtp_username'], emailconf['Smtp_password'])
        smtp.sendmail(sender, receiver, msgRoot.as_string())
        smtp.quit()

    def get_last_HtmlReport(self):
        '''获取最新的HtmlReport文件'''
        return self._get_lastfile(htmlreport_path)

    def get_last_ExcelReport(self):
        '''获取最新的Excel文件'''
        return self._get_lastfile(execlreport_path)

    def _get_lastfile(self, filedir):
        '''
        根据指定的目录获取最新的文件
        :param filedir: 指定的文件目录
        :return: 指定目录下的最新文件的绝对路径
        '''
        try:
            if os.path.exists(filedir):
                dirlist = os.listdir(filedir)
                self.lastfile = dirlist[-1]
                lastfile_path = os.path.join(filedir, self.lastfile)
                return lastfile_path
            else:
                print('指定的文件目录不正确.')
        except Exception as e:
            print(e)

    def chooseDirCases(self,casedir,pattern):
        '''
        根据指定目录获取匹配的测试用例
        :param casedir: 测试用例目录
        :param pattern: 匹配模式
        :return: 测试用例集
        '''
        casedirpath=os.path.join(testcase_path,'%s/'%casedir)
        discover_cases=unittest.defaultTestLoader.discover(casedirpath,pattern=pattern)
        return discover_cases

    def chooseAllCases(self,pattern):
        '''
        获取TestCases下所有的测试用例
        :param pattern: 匹配模式
        :return: 测试用例集
        '''
        discover_all_cases=unittest.defaultTestLoader.discover(testcase_path,pattern=pattern,top_level_dir=None)
        return discover_all_cases

    def createHTMLTestReport(self,title,desc,suite=None):
        '''
        执行用例并生成Html自动化测试报告
        :param title: 测试报告标题
        :param desc: 测试报告介绍
        :param suite: 用例装载集
        '''
        try:
            #设定html测试报告文件名称和路径
            nowtime=time.strftime("%Y-%m-%d-%H-%M-%S")
            report_name='HTReport_%s.html'%nowtime
            report_path=os.path.join(htmlreport_path,report_name)

            #判断是否存在相同文件，有则先删除
            if os.path.exists(report_path):
                os.remove(report_path)

            #运行测试并生成测试报告
            with open(report_path,'wb') as fp:
                runner=HTMLTestRunner(fp,title=title,description=desc)
                runner.run(suite)
        except Exception as e:
            print('[Error] HTMLTestReport自动化测试报告生成有误.具体错误为:%s'%e)

    def createBeautifulReport(self,title,suite):
        '''
        创建美化的html测试报告
        :param title: 测试报告标题
        :param suite: 用例集
        '''
        try:
            #设定html测试报告文件名称
            nowtime=time.strftime('%Y-%m-%d-%H-%M-%S')
            report_name='BFReport_%s.html'%nowtime
            report_path=os.path.join(htmlreport_path,report_name)

            #判断是否存在相同文件，有则先删除
            if os.path.exists(report_path):
                os.remove(report_path)

            #运行测试并生成测试报告
            runcase=BeautifulReport(suite)
            runcase.report(description=title,filename=report_name,log_path=htmlreport_path)
        except Exception as e:
            print('[Error] BeautifulReport自动化测试报告生成有误.具体错误为:%s' % e)





if __name__=="__main__":
    runtools=RunTools()
    b=runtools.chooseAllCases('test*.py')
    print(b)