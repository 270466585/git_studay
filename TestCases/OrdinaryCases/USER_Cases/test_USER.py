#!/user/bin/env python
#!encoding=utf-8
import json
import random
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''用户类api接口测试'''

class API_USER(unittest.TestCase):
    '''用户类api接口测试'''
    @classmethod
    def setUpClass(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db = DataBaseTools()
        self.api = CommonApiTools()
        self.api.login_api_pwd()        #密码登陆
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[USER_api_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.api.logout_api()                  #注销退出
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[USER_api_end]<<<<<<<<<<<<<<<<<<<<')

    def test_001_getuserinfo_byuserid(self):
        '''用户类-获取用户公开信息（通过userid）'''
        casename='获取用户公开信息-通过userid'
        api=self.yaml.get_USERapi(0)
        sql='select * from userlogin;'
        #获取数据库信息
        sqldata=self.db.get_selectdata_row(sql,0)
        userid=sqldata[3]
        mobile=sqldata[0]
        data={'userid':userid}
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result']['mobile'],mobile)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_002_getuserinfo_bymobile(self):
        '''用户类-获取用户公开信息（通过mobile）'''
        casename='获取用户公开信息-通过mobile'
        api=self.yaml.get_USERapi(0)
        sql='select * from userlogin;'
        sqldata=self.db.get_selectdata_row(sql,0)
        userid=sqldata[3]
        mobile=sqldata[0]
        data={'mobile':mobile}
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result']['userid'],userid)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_003_getuserinfo_byall(self):
        '''用户类-获取用户公开信息（通过userid和mobile）'''
        casename='获取用户公开信息-通过userid/mobile'
        api=self.yaml.get_USERapi(0)
        sql='select * from userlogin;'
        sqldata=self.db.get_selectdata_row(sql,0)
        userid=sqldata[3]
        mobile=sqldata[0]
        data={'userid':userid,'mobile':mobile}
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result']['mobile'],mobile)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_004_updateinfo(self):
        '''用户类-更新用户信息'''
        casename='更新用户信息'
        api=self.yaml.get_USERapi(2)
        sql1='select * from userlogin;'
        sql1data=self.db.get_selectdata_row(sql1,0)
        #获取数据信息
        userid=sql1data[3]
        mobile=sql1data[0]
        username=sql1data[8]
        city='ChengDu'
        phoneid=sql1data[4]
        jpushregisterid='lzl198903017'
        password=sql1data[1]
        gendor=random.randint(0,3)
        introduction='Hello!I am bear,I am doing api autotest!'
        body={'userid':userid,'mobile':mobile,'username':username,'city':city,'phoneid':phoneid,
              'jpushregisterid':jpushregisterid,'password':password,'gendor':gendor,'introduction':introduction}
        try:
            result=self.req.put_method(api,casename,body)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],0)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库--userinfo
            sql2='update userinfo set userid=\'%s\',username=\'%s\',mobile=\'%s\',city=\'%s\',phoneid=\'%s\',' \
                 'jpushregisterid=\'%s\',password=\'%s\',gendor=\'%d\',introduction=\'%s\' where infoid=1;'\
                 %(userid,username,mobile,city,phoneid,jpushregisterid,password,gendor,introduction)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_005_uploadcontacts(self):
        '''用户类-上传通讯录'''
        casename='上传通讯录'
        api=self.yaml.get_USERapi(5)
        sql='select * from userlogin;'
        #配置数据
        token=self.db.get_specific_data(sql,0,6)
        contactslist=[{'mobile':'13828836568','name':'feifei'},{'mobile':'13921342314','name':'nannan'}]
        contactsjson=json.dumps(contactslist)
        data='token=%s'%token
        try:
            result=self.req.post_method('urlencode',api,casename,data,contactsjson)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_006_getcontacts(self):
        '''用户类-获取用户通讯录'''
        casename='获取用户通讯录'
        api=self.yaml.get_USERapi(6)
        sql='select * from userlogin;'
        #配置数据
        token=self.db.get_specific_data(sql,0,6)
        data={'token':token}
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s-[Result]:FAILED]'%casename)
            self.log.info('-'*60)
            raise

    def test_007_finduser(self):
        '''用户类-查找嘟嘟用户'''
        casename='查找嘟嘟用户'
        api=self.yaml.get_USERapi(1)
        sql='select * from userlogin;'
        #配置数据
        token=self.db.get_specific_data(sql,0,6)
        key='王'
        data={'token':token,'key':key}
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

    def test_008_updateintroduction(self):
        '''用户类-更新签名信息'''
        casename='更新签名信息'
        api=self.yaml.get_USERapi(3)
        sql1='select * from userlogin;'
        #获取数据信息
        token=self.db.get_specific_data(sql1,0,6)
        introduction='好好学习，天天向上！'
        data='token=%s&introduction=%s'%(token,introduction)
        # 发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_009_bindbluetooth(self):
        '''用户类-更新绑定蓝牙'''
        casename='更新绑定蓝牙'
        api=self.yaml.get_USERapi(7)
        sql='select * from userlogin;'
        #获取数据信息
        token=self.db.get_specific_data(sql,0,6)
        bluetooth='5065832AD0A9'
        data='token=%s&bluetooth=%s'%(token,bluetooth)
        # 发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_010_unbindbluetooth(self):
        '''用户类-取消绑定蓝牙'''
        casename='取消绑定蓝牙'
        api=self.yaml.get_USERapi(7)
        sql='select * from userlogin;'
        #获取数据信息
        token=self.db.get_specific_data(sql,0,6)
        bluetooth = ''
        data='token=%s&bluetooth=%s'%(token,bluetooth)
        # 发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            raise

    def test_011_updateoftenplace(self):
        '''用户类-更新我的导航收藏'''
        casename='更新我的导航收藏'
        api=self.yaml.get_USERapi(8)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        bodylist=[{"title" : "公司","address" : "月光流域","datatype" : "history","longitude" : "123.422","latitude" : "22.2322","updatetime" : 2122212122},{"title" : "家","address" : "华侨城","datatype" : "favorite","longitude" : "123.4","latitude" : "22.23","updatetime" : 21212122}]
        data='userid=%s'%userid
        # 发送请求
        try:
            result=self.req.put_method(api,casename,bodylist,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_012_getoftenplace(self):
        '''用户类-获取我的导航收藏'''
        casename='获取我的导航收藏'
        api=self.yaml.get_USERapi(9)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        data={'userid':userid}
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

    def test_013_updatechatrecord(self):
        '''用户类-更新会话记录'''
        casename='更新会话记录'
        api=self.yaml.get_USERapi(10)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        bodylist=[{"type" : "channel","objid" : "10012","objname" : "中华大帝国频道","logourl" :"http://120.76.194.47:8888/group1/M00/00/05/eEzCL1haOg_Ew5gSAACvGaRuld0687.png","chattime" : 21222121}]
        data='userid=%s'%userid
        # 发送请求
        try:
            result=self.req.put_method(api,casename,body=bodylist,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_014_getchatrecord(self):
        '''用户类-获取会话记录'''
        casename='获取会话记录'
        api=self.yaml.get_USERapi(11)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        data={'userid':userid}
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

    def test_015_chatrecord_add(self):
        '''用户类-更新会话增量模式--新增会话记录'''
        casename='更新会话增量模式--新增会话记录'
        api=self.yaml.get_USERapi(12)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        mode='i'
        bodylist=[{"type" : "channel","objid" : "10012","objname" : "中华大帝国频道","logourl" :"http://120.76.194.47:8888/group1/M00/00/05/eEzCL1haOg_Ew5gSAACvGaRuld0687.png","chattime" : 21222121}]
        #配置参数
        data='userid=%s&mode=%s'%(userid,mode)
        # 发送请求
        try:
            result=self.req.put_method(api,casename,bodylist,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_016_chatrecord_update(self):
        '''用户类-更新会话增量模式--更新会话记录'''
        casename='更新会话增量模式--更新会话记录'
        api=self.yaml.get_USERapi(12)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        mode='u'
        bodylist=[{"type" : "channel","objid" : "10012","objname" : "中华大帝国频道","logourl" :"http://120.76.194.47:8888/group1/M00/00/05/eEzCL1haOg_Ew5gSAACvGaRuld0687.png","chattime" : 21222233}]
        #配置参数
        data='userid=%s&mode=%s'%(userid,mode)
        # 发送请求
        try:
            result=self.req.put_method(api,casename,bodylist,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_017_chatrecord_delete(self):
        '''用户类-更新会话增量模式--删除会话记录'''
        casename='更新会话增量模式--删除会话记录'
        api=self.yaml.get_USERapi(12)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        mode='d'
        bodylist=[{"type" : "channel","objid" : "10012","objname" : "中华大帝国频道","logourl" :"http://120.76.194.47:8888/group1/M00/00/05/eEzCL1haOg_Ew5gSAACvGaRuld0687.png","chattime" : 21222233}]
        #配置参数
        data='userid=%s&mode=%s'%(userid,mode)
        # 发送请求
        try:
            result=self.req.put_method(api,casename,bodylist,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            raise

if __name__=="__main__":
    unittest.main()