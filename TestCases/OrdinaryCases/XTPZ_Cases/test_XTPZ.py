#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools

'''系统配置类api'''

class API_XTPZ(unittest.TestCase):
    '''系统配置类api接口测试'''
    @classmethod
    def setUpClass(self):
        self.log=LogTools()
        self.yaml=YamlTools()
        self.req=RequestTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[XTPZ_api_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[XTPZ_api_end]<<<<<<<<<<<<<<<<<<<<<<')

    def test_001_getSysTime(self):
        '''系统配置类-获取系统时间'''
        casename='获取系统时间'
        api=self.yaml.get_XTPZapi(0)
        # 发送请求
        try:
            result=self.req.get_method(api,casename)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_002_getSysErrorCode(self):
        '''系统配置类-获取系统错误码映射'''
        casename='获取错误码映射'
        api=self.yaml.get_XTPZapi(1)
        # 发送请求
        try:
            result=self.req.get_method(api,casename)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_003_getVersion(self):
        '''系统配置类-获取系统版本信息'''
        data={'innerver':'2000','appid':'iosapp'}
        casename='获取版本信息'
        api=self.yaml.get_XTPZapi(3)
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS' % casename)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            raise

if __name__=="__main__":
    unittest.main()