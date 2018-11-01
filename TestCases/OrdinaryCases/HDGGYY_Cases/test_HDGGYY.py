#!/user/bin/env python
#!encoding=utf-8
import random
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''活动广告运营api接口测试'''

class API_HDGGYY(unittest.TestCase):
    '''活动广告运营api接口测试'''
    @classmethod
    def setUpClass(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db = DataBaseTools()
        self.api = CommonApiTools()
        self.api.login_api_pwd()  # 密码登陆
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[SJCJ_api_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.api.logout_api()  # 注销退出
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[SJCJ_api_end]<<<<<<<<<<<<<<<<<<<<')

    def test_001_getadv(self):
        '''活动广告运营类-取得当前用户相关的广告列表'''
        casename='获取当前用户广告列表'
        api=self.yaml.get_HDGGYYapi(0)
        sql='select * from userlogin;'
        #获取数据
        token=self.db.get_specific_data(sql,0,6)
        data={'token':token}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_002_signin(self):
        '''活动广告运营类-用户签到，并获得连续打卡天数'''
        casename='获取用户连续打卡天数'
        api=self.yaml.get_HDGGYYapi(1)
        sql='select * from userlogin;'
        # 获取数据
        token=self.db.get_specific_data(sql, 0, 6)
        data='token=%s'%token
        # 发送请求
        try:
            result=self.req.post_method('urlencode',api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_003_sendfeedback(self):
        '''活动广告运营类-用户提交问题建议'''
        casename='用户提交问题建议'
        api=self.yaml.get_HDGGYYapi(2)
        sql='select * from userlogin;'
        #获取数据
        userid=self.db.get_specific_data(sql,0,3)
        contactinfo='QQ:14298246'
        content='接口测试!'
        data={'userid':userid,'contactinfo':contactinfo,'content':content}
        # 发送请求
        try:
            result=self.req.post_method('json',api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result'],userid)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_004_getfeedback(self):
        '''活动广告运营类-用户取得自己提交的问题的反馈'''
        casename='用户取得自己提交的问题的反馈'
        api=self.yaml.get_HDGGYYapi(3)
        sql='select * from userlogin;'
        #获取数据
        token=self.db.get_specific_data(sql,0,6)
        data={'token':token}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库信息
            sql2='update feedback set feedid=\'%s\' where userid=\'%s\';'%(result['result'][0]['feedid'],result['result'][0]['userid'])
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_005_gettrack(self):
        '''活动广告运营类-获取建议回复信息'''
        casename='获取建议回复信息'
        api=self.yaml.get_HDGGYYapi(4)
        sql='select * from feedback;'
        #获取数据
        feedid=self.db.get_specific_data(sql,0,2)
        data={'feedid':feedid}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_006_givestar(self):
        '''活动广告运营类-给予客服评级'''
        casename='给予客服评级'
        api=self.yaml.get_HDGGYYapi(5)
        sql='select * from feedback;'
        #获取数据
        feedid=self.db.get_specific_data(sql,0,2)
        rate=random.randint(1,6)       #1-5星评级
        data='feedid=%s&rate=%s'%(feedid,rate)
        # 发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            raise

if __name__=="__main__":
    unittest.main()