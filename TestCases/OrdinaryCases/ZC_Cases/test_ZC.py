#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools

'''注册类api测试'''

class API_ZC(unittest.TestCase):
    '''注册类api接口测试'''
    @classmethod
    def setUpClass(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db=DataBaseTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[ZC_api_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.db.cur_close()         #关闭游标
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[ZC_api_end]<<<<<<<<<<<<<<<<<<<<<<')

    def test_001_getfzcid(self):
        '''获取非注册用户标识id'''
        casename='获取非注册用户标识id'
        sql1='select * from userregister;'
        phoneid=self.db.get_specific_data(sql1,0,6)   #从数据库中获取手机号码数据
        api=self.yaml.get_ZCapi(0)
        data={'phoneid':phoneid}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库fzcuid字段
            sql2='update userregister set fzcuid=\'%s\' where phoneid=\'%s\''%(result['result'],phoneid)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_002_getverifycode(self):
        '''获取验证码'''
        casename='获取验证码'
        api=self.yaml.get_ZCapi(2)
        sql1='select * from verifycode;'
        telnum=self.db.get_specific_data(sql1,0,0)  #从数据库中获取手机号数据
        data={'mobile':telnum,'isregister':1}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库verifycode字段
            sql2='update verifycode set verifycode=\'%s\' where telnum=\'%s\''%(result['result'],telnum)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_003_register(self):
        '''正式注册'''
        casename='正式注册'
        api=self.yaml.get_ZCapi(1)
        sql1='select * from userregister;'
        sql2='select * from verifycode;'
        #获取数据信息--tuple
        sql1data=self.db.get_selectdata_row(sql1,0)
        sql2data=self.db.get_selectdata_row(sql2,0)
        #获取数据库数据信息
        username=sql1data[1]
        password=sql1data[3]
        fzcuid=sql1data[4]
        telnum=sql2data[0]
        verifycode=sql2data[1]
        data={"userid":fzcuid,"username":username,"mobile":telnum,"password":password,"validcode":verifycode}

        # 发送请求
        try:
            result=self.req.post_method('json',api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            #更新数据库内容--注册领驭号
            sql3='update userregister set zcuid=\'%s\' where telnum=\'%s\';'%(result['result'],telnum)
            sql4='update userlogin set zcuid=\'%s\' where telnum=\'%s\';' % (result['result'], telnum)
            #更新用户注册状态
            sql5='update userregister set zcbz=1 where telnum=\'%s\';'%telnum
            self.db.execute_sql(sql3)
            self.db.execute_sql(sql4)
            self.db.execute_sql(sql5)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            raise


if __name__=="__main__":
    unittest.main()