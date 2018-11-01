#!/user/bin/env python
#!encoding=utf-8
import configparser

'''重写configparser，控制大小写自动转化'''

class RewriteConfigParser(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        '''改写optionxform，废除大小写转化'''
        return optionstr
