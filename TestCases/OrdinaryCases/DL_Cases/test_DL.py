#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''登录类api接口测试'''

class API_DL(unittest.TestCase):
    '''登录类api接口测试'''
    def setUp(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db = DataBaseTools()
        self.api= CommonApiTools()

    def tearDown(self):
        self.db.cur_close()     # 关闭游标
        self.api.logout_api()   # 退出登陆

    def test_001_loginbypassword_uid(self):
        '''用户登录类-密码方式登陆认证(通过uid以及password进行登陆)'''
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[DL_api_start]<<<<<<<<<<<<<<<<<<<<')
        casename='密码方式登陆认证_uid认证'
        api=self.yaml.get_DLapi(0)
        sql1='select * from userlogin;'
        sql1data=self.db.get_selectdata_row(sql1,0)
        #获取数据库数据
        zcuid=sql1data[2]
        password=sql1data[1]
        phoneid=sql1data[4]
        data={'userid':zcuid,'pwd':password,'phoneid':phoneid}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库信息--用户领驭号、token
            sql2='update userlogin set dlbz=1,userid=\'%s\',token=\'%s\' where phoneid=\'%s\';'\
                 %(result['result']['userid'],result['result']['token'],phoneid)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_002_loginbypassword_mobile(self):
        '''用户登录类-密码方式登陆认证(通过mobile以及password进行登陆)'''
        casename='密码方式登陆认证_mobile认证'
        api=self.yaml.get_DLapi(0)
        sql1='select * from userlogin;'
        sql1data=self.db.get_selectdata_row(sql1,0)
        #获取数据库数据
        mobile=sql1data[0]
        password=sql1data[1]
        phoneid=sql1data[4]
        data={'mobile':mobile,'pwd':password,'phoneid':phoneid}

        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
            #更新数据库信息--用户领驭号、token
            sql2 = 'update userlogin set dlbz=1,userid=\'%s\',token=\'%s\' where phoneid=\'%s\';' \
               % (result['result']['userid'], result['result']['token'], phoneid)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_003_loginbypassword_uid_mobile(self):
        '''用户登录类-密码方式登陆认证(通过uid、mobile以及password进行登陆)'''
        casename='密码方式登陆认证_uid/mobile认证'
        api=self.yaml.get_DLapi(0)
        sql1='select * from userlogin;'
        sql1data=self.db.get_selectdata_row(sql1,0)
        #获取数据库数据
        zcuid=sql1data[2]
        mobile=sql1data[0]
        password =sql1data[1]
        phoneid =sql1data[4]
        data={'userid':zcuid,'mobile':mobile,'pwd':password,'phoneid':phoneid}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True)
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
            #更新数据库信息--用户领驭号、token
            sql2 = 'update userlogin set dlbz=1,userid=\'%s\',token=\'%s\' where phoneid=\'%s\';' \
               % (result['result']['userid'], result['result']['token'], phoneid)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_004_loginbyverifycode(self):
        '''用户登录类-验证码方式登陆认证'''
        casename='验证码方式登陆认证'
        api=self.yaml.get_DLapi(1)
        #获取登陆验证码
        self.api.get_verifycode(0)
        #获取数据库数据
        sql1='select * from userlogin;'
        sql1data=self.db.get_selectdata_row(sql1,0)
        telnum=sql1data[0]
        loginverifycode=sql1data[7]
        phoneid=sql1data[4]
        data={'mobile':telnum,'validcode':loginverifycode,'phoneid':phoneid}

        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
            # 更新数据库信息--用户领驭号、token、登陆标志
            sql2 = 'update userlogin set dlbz=1,userid=\'%s\',token=\'%s\' where phoneid=\'%s\';' \
                   % (result['result']['userid'], result['result']['token'], phoneid)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_005_checkmobile(self):
        '''用户登录类-检查手机号码是否注册(手机号码已经注册)'''
        casename='检查手机号码是否注册-已经注册'
        sql='select * from userlogin;'
        #获取数据
        telnum=self.db.get_specific_data(sql,0,0)
        api=self.yaml.get_DLapi(2)
        data={'mobile':telnum}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'该手机号码已经注册！')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-' * 60)
            raise

    def test_006_checkmoblie(self):
        '''用户登录类-检查手机号码是否注册(手机号码未注册)'''
        casename='检查手机号码是否注册-未注册'
        sql='select * from userlogin;'
        #获取数据
        telnum=self.db.get_specific_data(sql,1,0)
        api=self.yaml.get_DLapi(2)
        data={'mobile':telnum}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],10351) and self.assertEqual(result['isTrue'],False) and self.assertEqual(result['errorMessage'],'该手机未注册')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('>>>>>>>>>>>>>>>>>>>>>[DL_api_end]<<<<<<<<<<<<<<<<<<<<<<')
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('>>>>>>>>>>>>>>>>>>>>>[DL_api_end]<<<<<<<<<<<<<<<<<<<<<<')
            raise


if __name__=="__main__":
    unittest.main()