#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''好友类api接口测试'''

class API_HY(unittest.TestCase):
    '''好友类api接口测试'''
    @classmethod
    def setUpClass(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db = DataBaseTools()
        self.api = CommonApiTools()
        self.api.login_api_pwd()  # 密码登陆
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[HY_api_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.api.logout_api()  # 注销退出
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[HY_api_end]<<<<<<<<<<<<<<<<<<<<')

    def test_001_friendsinfo_userid(self):
        '''好友类-获取好友信息(通过userid)'''
        casename='获取好友信息-userid'
        api=self.yaml.get_HYapi(6)
        sql='select * from userlogin;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        userid=sqldata[3]
        token=sqldata[6]
        data={'userid':userid,'token':token}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result']['userid'],userid)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_002_friendinfo_mobile(self):
        '''好友类-获取好友信息（通过mobile）'''
        casename='获取好友信息-mobile'
        api=self.yaml.get_HYapi(6)
        sql='select * from userlogin;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[6]
        mobile=sqldata[0]
        data={'token':token,'mobile':mobile}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) and self.assertEqual(result['result']['mobile'], mobile)
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_003_friendinfo_useridmobile(self):
        '''好友类-获取好友信息（通过userid/mobile）'''
        casename='获取好友信息-userid/mobile'
        api=self.yaml.get_HYapi(6)
        sql='select * from userlogin;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[6]
        userid=sqldata[3]
        mobile=sqldata[0]
        data={'token':token,'userid':userid,'mobile':mobile}
        # 发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertSequenceEqual(result['isTrue'],True) and self.assertSequenceEqual(result['result']['userid'],userid) and self.assertSequenceEqual(result['result']['mobile'],mobile)
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_004_addfriends(self):
        '''好友类-向指定用户申请成为好友'''
        casename='向指定用户申请成为好友'
        api=self.yaml.get_HYapi(0)
        sql='select * from userlogin;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[6]
        friendid='user10020'
        info='123'
        data='token=%s&friendid=%s&info=%s'%('123456',friendid,info)
        #发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertSequenceEqual(result['errorMessage'],'申请成功，请耐心等待对方确认。')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_005_myaddlist(self):
        '''好友类-取得向我提出加好友申请的用户列表'''
        casename='获取添加自己的用户列表'
        api=self.yaml.get_HYapi(1)
        sql='select * from userlogin;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[6]
        userid=sqldata[3]
        data={'token':'123456','userid':userid}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],10304) and self.assertEqual(result['isTrue'],False) and self.assertSequenceEqual(result['errorMessage'],'用户不存在')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_006_deletefriend(self):
        '''好友类-删除指定好友'''
        casename='删除指定好友'
        api=self.yaml.get_HYapi(5)
        sql='select * from userlogin;'
        #获取数据
        sqldata = self.db.get_selectdata_row(sql, 0)
        token = sqldata[6]
        friendid='user10001'
        data='token=%s&friendid=%s'%(token,friendid)
        #发送请求
        try:
            result=self.req.delete_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'删除好友成功')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_007_getfriendslist(self):
        '''好友类-获得我的好友列表'''
        casename='获得我的好友列表'
        api=self.yaml.get_HYapi(7)
        sql='select * from userlogin;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[6]
        userid=sqldata[3]
        data={'token':token,'userid':userid}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],10306) and self.assertEqual(result['errorMessage'],'好友不存在')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_008_nickname(self):
        '''好友类-为我的好友设置昵称'''
        casename='为我的好友设置昵称'
        api=self.yaml.get_HYapi(8)
        sql='select * from userlogin;'
        #获取数据
        sqldata = self.db.get_selectdata_row(sql, 0)
        token = sqldata[6]
        userid = sqldata[3]
        friendid='user10033'
        name='戴眼镜的熊'
        data='token=%s&friendid=%s&name=%s'%(token,friendid,name)
        #发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'更新昵称成功')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_009_newmessage(self):
        '''好友类-取得待处理好友消息'''
        casename='取得待处理好友消息'
        api=self.yaml.get_HYapi(11)
        sql='select * from userlogin;'
        #获取数据
        token=self.db.get_specific_data(sql,0,6)
        data={'token':token}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'], 10811) and self.assertEqual(result['errorMessage'], '没有新的朋友消息')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_010_search(self):
        '''好友类-搜索引擎'''
        casename='搜索引擎'
        api=self.yaml.get_HYapi(12)
        sql='select * from userlogin;'
        #获取数据
        token=self.db.get_specific_data(sql,0,6)
        type='all'
        key='王'
        data={'token':token,'type':type,'key':key}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            raise

if __name__=="__main__":
    unittest.main()










