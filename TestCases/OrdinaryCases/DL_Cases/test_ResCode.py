#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''校验注册验证码api接口测试'''

class API_ResCode(unittest.TestCase):
    '''校验注册验证码api接口测试'''
    def setUp(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db = DataBaseTools()
        self.api = CommonApiTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[ResCode_api_start]<<<<<<<<<<<<<<<<<<<<')

    def tearDown(self):
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[ResCode_api_end]<<<<<<<<<<<<<<<<<<<<')

    def test_001_check_registercode(self):
        '''用户登录类-校验注册验证码'''
        casename='校验注册验证码'
        sql='select * from verifycode;'
        api=self.yaml.get_DLapi(3)
        #校验注册验证码
        self.api.get_verifycode(1)
        sqldata=self.db.get_selectdata_row(sql,1)
        #获取数据
        telnum=sqldata[0]
        res_code=sqldata[1]
        data={'mobile':telnum,'validcode':res_code}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'验证码正确！')
            self.log.info('[%s]-[Result]:PASS'%casename)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            raise

if __name__=="__main__":
    unittest.main()