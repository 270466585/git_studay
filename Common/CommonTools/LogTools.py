#!/user/bin/env python
#!encoding=utf-8
import logging
import os
import sys
import time
from Common.CommonTools.PathTools import log_path

'''日志相关封装方法'''

class LogTools:
    def __init__(self):
        '''设置文件路径、日志等级、日志输出格式'''
        self.logfile=os.path.join(log_path,'%s.log'%self.nowtime())
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.format=logging.Formatter('[%(asctime)s]-[%(levelname)s]-%(message)s')
        # 获取当前调用函数的类的名称
        self.log_cur_name = str(sys._getframe().f_back.f_code.co_name)

    def __console(self,loglevel,message):
        '''设置本地与日志输出'''
        #创建一个FileHandler，用于本地日志输出
        fh=logging.FileHandler(self.logfile,'a',encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.format)
        self.logger.addHandler(fh)

        #创建一个StreamHandler，用于控制台输出
        sh=logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(self.format)
        self.logger.addHandler(sh)

        #通过判断level输出
        if loglevel=='info':
            self.logger.info("".join(["run:",message]))
        elif loglevel=='debug':
            self.logger.debug("".join(["run:",message]))
        elif loglevel=='warning':
            self.logger.warning("".join(["run:",message]))
        elif loglevel=='error':
            self.logger.error("".join(["run:",message]))

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(sh)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def info(self,message):
        '''输出info信息'''
        self.__console('info',message)

    def debug(self,message):
        '''输出debug信息'''
        self.__console('debug',message)

    def warning(self,message):
        '''输出warning信息'''
        self.__console('warning',message)

    def error(self,message):
        '''输出error信息'''
        self.__console('error',message)

    def nowtime(self):
        '''获取当前时间'''
        nowtime=time.strftime("%Y-%m-%d")
        return nowtime

    def _logcurname(self):
        '''获取调用当前函数的类的名称'''
        return str(sys._getframe().f_back.f_code.co_name)


if __name__=="__main__":
    log=LogTools()
    log.info('nihao')
    log.debug('lalala')
