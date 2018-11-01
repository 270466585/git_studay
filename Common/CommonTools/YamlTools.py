#!/user/bin/env python
#!encoding=utf-8
import yaml
from Common.CommonTools.PathTools import yaml_path

'''yaml文件读取函数'''

class YamlTools:
    def readyaml(self):
        '''读取yaml配置文件,返回URL下的数据信息(字典类型)'''
        try:
            with open(yaml_path,'r',encoding='utf-8') as url:
                url_data=yaml.load(url)
            return url_data['URL']
        except Exception as e:
            print(e)
            print('未找到.yaml文件')


    def _getapi(self,part,index):
        '''
        返回yaml文件指定part下的api
        :param part:URL下的api类型part，类似于XTPZ
        :param index:通过角标获取指定的api值
        :return:指定的api的值
        '''
        try:
            url_data=self.readyaml()
            return url_data[part][index]
        except:
            print('【%s】部分下的api获取失败.'%part)


    def get_XTPZapi(self,index):
        '''获取系统配置类api'''
        return self._getapi('XTPZ',index)

    def get_ZCapi(self,index):
        '''获取注册类api'''
        return self._getapi('ZC',index)

    def get_DLapi(self,index):
        '''获取登录类api'''
        return self._getapi('DL',index)

    def get_TCapi(self,index):
        '''获取退出类api'''
        return self._getapi('TC',index)

    def get_USERapi(self,index):
        '''获取用户类api'''
        return self._getapi('USER',index)

    def get_SJCJapi(self,index):
        '''获取数据采集类api'''
        return self._getapi('SJCJ',index)

    def get_HDGGYYapi(self,index):
        '''获取活动广告运营类api'''
        return self._getapi('HDGGYY',index)

    def get_WJGJapi(self,index):
        '''获取文件处理/工具类api'''
        return self._getapi('WJGJ',index)

    def get_HYapi(self,index):
        '''获取好友类api'''
        return self._getapi('HY',index)

    def get_PDDTapi(self,index):
        '''获取频道电台类api'''
        return self._getapi('PDDT',index)






if __name__=="__main__":
    api=YamlTools()
    b=api.readyaml()
    print(api.get_XTPZapi(0))
    print(api.get_DLapi(0))
    print(api.get_HDGGYYapi(0))
    print(api.get_HYapi(0))
    print(api.get_PDDTapi(0))
    print(api.get_SJCJapi(0))
    print(api.get_TCapi(0))
    print(api.get_USERapi(0))
    print(api.get_ZCapi(0))
    print(api.get_XTPZapi(0))
    print(b)
