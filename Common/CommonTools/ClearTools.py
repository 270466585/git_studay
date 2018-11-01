#!/user/bin/env python
#!encoding=utf-8
from Common.CommonTools.PathTools import *

'''公共方法函数封装'''


class ClearTools:
    def clear_logs(self):
        '''一键清空所有日志文件'''
        # 循环删除Log目录下的日志文件
        for i in os.listdir(log_path):
            getfile = os.path.join(log_path, i)
            os.remove(getfile)

        # 判断Log目录下的日志文件是否全部删除
        if len(os.listdir(log_path)) == 0:
            print('Log日志文件已清理完毕.')

    def clear_Htmlreports(self):
        '''一键清空所有HTML报告文件'''
        #循环删除Report目录下的报告文件
        for i in os.listdir(htmlreport_path):
            getfile=os.path.join(htmlreport_path,i)
            os.remove(getfile)

        #判断Report目录下的报告文件是否全部删除
        if len(os.listdir(htmlreport_path))==0:
            print('HTML测试报告文件已清理完毕.')

    def clear_Excelreports(self):
        '''一键清空所有Excel报告文件'''
        #循环删除Report目录下的报告文件
        for i in os.listdir(execlreport_path):
            getfile=os.path.join(execlreport_path,i)
            os.remove(getfile)

        #判断Report目录下的报告文件是否全部删除
        if len(os.listdir(execlreport_path))==0:
            print('Excel测试报告文件已清理完毕.')




if __name__=="__main__":
    commontools=ClearTools()
    commontools.clear_Htmlreports()
    commontools.clear_logs()
    commontools.clear_Excelreports()
