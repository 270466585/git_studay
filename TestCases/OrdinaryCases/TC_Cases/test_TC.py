#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''退出类api接口测试'''

class API_TC(unittest.TestCase):
    '''退出注销类api接口测试'''
    def setUp(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db = DataBaseTools()
        self.api = CommonApiTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[TC_api_start]<<<<<<<<<<<<<<<<<<<<')

    def tearDown(self):
        self.db.cur_close()     #关闭游标
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[TC_api_end]<<<<<<<<<<<<<<<<<<<<<<')

    def test_1_logout(self):
        '''退出注销类-退出注销'''
        casename='退出注销'
        api=self.yaml.get_TCapi(0)
        #获取数据
        sql1='select * from userlogin;'
        userid=self.db.get_specific_data(sql1,0,3)
        # 发送请求
        try:
            self.api.login_api_pwd()        #先登录
            data ='userid=%s'%userid
            result=self.req.post_method('urlencode',api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'退出登录成功！')
            self.log.info('[%s]-[Result]:PASS'%casename)
            #更新登陆状态
            sql2='update userlogin set dlbz=0 where userid=\'%s\';'%userid
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            raise

if __name__=="__main__":
    unittest.main()