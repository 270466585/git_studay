#!/user/bin/env python
#!encoding=utf-8
from Common.CommonTools.PathTools import config_path
from Common.CommonTools.RewriteConfigparser import RewriteConfigParser

# #改变标准输出默认编码为gb18030（gbk）
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

'''读取配置文件相关公共方法'''

class ConfigReadTools:
    def __init__(self,filepath):
        '''读取配置文件'''
        self.filepath=filepath
        self.readconf=RewriteConfigParser()
        self.readconf.read(self.filepath)

    def get_conf_all_sections(self):
        '''获取所有的sections'''
        return self.readconf.sections()

    def get_conf_all_options(self,section):
        '''获取指定section下的所有options'''
        return self.readconf.options(section)

    def get_section_item(self,section):
        '''获取指定section的option的item(字典形式)'''
        return dict(self.readconf.items(section))

    def get_option_value(self,section,key):
        '''获取指定section下指定option的value'''
        return self.readconf.get(section,key)

    def get_conf_dumps_dict(self):
        '''获取配置文件的所有sections和options和value,并以字典形式展示'''
        #获取config配置文件的所有sections
        all_sections=self.readconf.sections()
        dumps_dict={}
        for i in all_sections:
            #将每个section下的option和value以字典形式获取
            items=dict(self.readconf.items(i))
            #组合成字典：格式为{section:{option:value}}
            dumps_dict[i]=items
        return dumps_dict

    def delete_section_item(self,section,key):
        '''删除指定section下的item'''
        self.readconf.remove_option(section,key)

    def delete_section(self,section):
        '''删除指定section'''
        self.readconf.remove_section(section)

    def add_section(self,section):
        '''添加一个section'''
        self.readconf.add_section(section)

    def add_item(self,section,key,value):
        '''针对一个指定的section添加key和value'''
        self.readconf.set(section,key,value)

    def conf_save(self):
        '''在内存中修改的内容写回文件中并自动关闭文件，相当于保存'''
        with open(self.filepath,'w') as FP:
            self.readconf.write(FP)

    def have_section(self,section):
        '''检查section是否存在,返回True/False'''
        return self.readconf.has_section(section)

    def have_option(self,section,key):
        '''检查指定section下option是否存在，返回True/False'''
        return self.readconf.has_option(section,key)



if __name__=='__main__':
    readconf=ConfigReadTools(config_path)
    a=readconf.get_conf_dumps_dict()
    print(a)
