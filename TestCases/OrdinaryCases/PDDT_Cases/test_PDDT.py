#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''频道电台类api接口测试'''

class API_PDDT(unittest.TestCase):
    '''频道电台类api接口测试'''
    @classmethod
    def setUpClass(self):
        self.log = LogTools()
        self.yaml = YamlTools()
        self.req = RequestTools()
        self.db = DataBaseTools()
        self.api = CommonApiTools()
        self.api.login_api_pwd()  # 密码登陆
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[PDDT_api_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.api.logout_api()  # 注销退出
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[PDDT_api_end]<<<<<<<<<<<<<<<<<<<<')

    def test_001_makechannel(self):
        '''频道电台类-创建频道(普通频道)'''
        casename='创建频道(普通频道)'
        api=self.yaml.get_PDDTapi(0)
        sql='select * from userlogin;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[6]
        userid=sqldata[3]
        data={"channelid" : "","channelname" : "接口测试","channelremark" : "","autoname" : 0,"ispublic" : 0,"logoid" : "","memberids" : ["user10400","user10430"],"owner" : userid,"token" : token}
        #发送请求
        try:
            result=self.req.post_method('json',api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库信息--channel
            sql2='update channel set channelid=\'%s\',owner=\'%s\',token=\'%s\',channelname=\'%s\' where cid=1'%\
                 (result['result']['channelid'],result['result']['owner'],result['result']['token'],result['result']['channelname'])
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_002_changenickname(self):
        '''频道电台类-更新自己的昵称'''
        casename='更新自己的昵称'
        api=self.yaml.get_PDDTapi(1)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        channelid=sqldata[1]
        userid=sqldata[2]
        name='王大锤'
        data='token=%s&channelid=%s&name=%s'%(token,channelid,name)
        #发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result'],userid)
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_003_changechannelname(self):
        '''频道电台类-管理员更新频道名称'''
        casename='管理员更新频道名称'
        api=self.yaml.get_PDDTapi(2)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        channelid=sqldata[1]
        userid=sqldata[2]
        name='我心飞翔'
        data='token=%s&channelid=%s&name=%s'%(token,channelid,name)
        #发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result'],userid)
            self.log.info('[%s]-[nfResult]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库--channel
            sql2='update channel set channelname=\'%s\' where owner=\'%s\';'%(name,userid)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-' * 60)
            raise

    def test_004_changeremark(self):
        '''频道电台类-管理员更新频道简介'''
        casename='管理员更新频道简介'
        api=self.yaml.get_PDDTapi(3)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        channelid=sqldata[1]
        userid=sqldata[2]
        remark='简介更新,接口测试!'
        data='token=%s&channelid=%s&remark=%s'%(token,channelid,remark)
        #发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['result'],userid)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
            #更新数据库--channel
            sql2='update channel set remark=\'%s\' where owner=\'%s\';'%(remark,userid)
            self.db.execute_sql(sql2)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_005_ispublic_yes(self):
        '''频道电台类-管理员更新频道不需验证申请'''
        casename='管理员更新频道不需验证申请'
        api=self.yaml.get_PDDTapi(4)
        sql='select * from channel;'
        # 获取数据
        sqldata=self.db.get_selectdata_row(sql, 0)
        token=sqldata[3]
        channelid=sqldata[1]
        userid=sqldata[2]
        ispublic=1
        data='token=%s&channelid=%s&ispublic=%s'%(token,channelid,ispublic)
        #发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and \
            self.assertEqual(result['errorMessage'],'更新频道成功') and self.assertSequenceEqual(result['result'],userid)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_006_ispublic_no(self):
        '''频道电台类-管理员更新频道需要验证申请'''
        casename = '管理员更新频道需要验证申请'
        api = self.yaml.get_PDDTapi(4)
        sql = 'select * from channel;'
        # 获取数据
        sqldata = self.db.get_selectdata_row(sql, 0)
        token = sqldata[3]
        channelid = sqldata[1]
        userid = sqldata[2]
        ispublic = 0
        data = 'token=%s&channelid=%s&ispublic=%s' % (token, channelid, ispublic)
        # 发送请求
        try:
            result = self.req.put_method(api, casename, data=data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) and \
            self.assertEqual(result['errorMessage'], '更新频道成功') and self.assertSequenceEqual(result['result'], userid)
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_007_batchadd(self):
        '''频道电台类-批量增加成员到频道中'''
        casename='批量增加成员到频道中'
        api=self.yaml.get_PDDTapi(6)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        channelid=sqldata[1]
        userid=sqldata[2]
        body={"channelid" : channelid,"memberlist" : ["user10400","user10430"],"userid" : userid,"token" : token}
        #发送请求
        try:
            result=self.req.put_method(api,casename,body)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) \
            and self.assertEqual(result['result'],userid)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_008_batchkick(self):
        '''频道电台类-从频道中批量删除成员'''
        casename='从频道中批量删除成员'
        api=self.yaml.get_PDDTapi(7)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        userid=sqldata[2]
        channelid=sqldata[1]
        body={"channelid" : channelid,"memberlist" : ["user10400","user10430"],"userid" : userid,"token" : token}
        #发送请求
        try:
            result=self.req.delete_method(api,casename,body=body)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) \
            and self.assertEqual(result['result'], userid)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_009_applychannel(self):
        '''频道电台类-申请加入频道(需审核)'''
        casename='申请加入频道(需审核)'
        api=self.yaml.get_PDDTapi(8)
        sql = 'select * from channel;'
        # 获取数据
        sqldata = self.db.get_selectdata_row(sql, 0)
        token=sqldata[3]
        userid=sqldata[2]
        channelid='10404'
        reason='申请加入，接口测试！'
        data='token=%s&channelid=%s&reason=%s'%(token,channelid,reason)
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) \
            and self.assertEqual(result['result'], userid)
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_010_addchannel(self):
        '''频道电台类-直接加入频道'''
        casename='直接加入频道'
        api=self.yaml.get_PDDTapi(9)
        sql='select * from channel;'
        #获取数据
        sqldata = self.db.get_selectdata_row(sql, 0)
        token = sqldata[3]
        userid = sqldata[2]
        channelid='10404'
        data='token=%s&channelid=%s'%(token,channelid)
        #发送请求
        try:
            result=self.req.put_method(api,casename,data=data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) \
            and self.assertEqual(result['result'], userid)
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_011_getmychannellist(self):
        '''频道电台类-取得自己的频道列表'''
        casename='取得我的频道列表'
        api=self.yaml.get_PDDTapi(14)
        sql='select * from channel;'
        #获取数据
        token=self.db.get_specific_data(sql,0,3)
        data={'token':token}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)\
            and self.assertEqual(result['errorMessage'],'操作成功')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_012_getmember(self):
        '''频道电台类-取得指定频道的成员列表'''
        casename='取得指定频道的成员列表'
        api=self.yaml.get_PDDTapi(15)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        channelid=sqldata[1]
        data={'token':token,'channelid':channelid}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)\
            and self.assertEqual(result['errorMessage'],'操作成功')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_013_applylist(self):
        '''频道电台类-获取所有自己创建的频道的相关信息'''
        casename='所有自己创建的频道的相关信息'
        api=self.yaml.get_PDDTapi(16)
        sql='select * from channel;'
        #获取数据
        token=self.db.get_specific_data(sql,0,3)
        data={'token':token}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) \
            and self.assertEqual(result['errorMessage'], '操作成功')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_014_searchchannel(self):
        '''频道电台类-查找频道'''
        casename='查找频道'
        api=self.yaml.get_PDDTapi(17)
        sql='select * from channel;'
        #获取数据
        token=self.db.get_specific_data(sql,0,3)
        key='罗'
        data={'token':token,'key':key}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'])
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_015_randomrecommend(self):
        '''频道电台类-随机推荐频道'''
        casename='随机推荐频道'
        api=self.yaml.get_PDDTapi(18)
        sql='select * from channel;'
        #获取数据
        token=self.db.get_specific_data(sql,0,3)
        maxnum=3
        data={'token':token,'maxnum':maxnum}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'])
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_016_getchannelinfo(self):
        '''频道电台类-获取指定频道详情'''
        casename='获取指定频道详情'
        api=self.yaml.get_PDDTapi(19)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        channelid=sqldata[1]
        data={'token':token,'channelid':channelid}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)\
            and self.assertEqual(result['errorMessage'],'操作成功')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_017_getchannelstatus(self):
        '''频道电台类-用户取得自己的频道的活跃统计'''
        casename='用户取得自己的频道的活跃统计'
        api=self.yaml.get_PDDTapi(21)
        sql='select * from channel;'
        #获取数据
        token=self.db.get_specific_data(sql,0,3)
        data={'token':token}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) \
            and self.assertEqual(result['errorMessage'], '操作成功')
            self.log.info('[%s]-[Result]:PASS' % casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED' % casename)
            self.log.info('-' * 60)
            raise

    def test_018_getlogo(self):
        '''频道电台类-获取频道logo图片'''
        casename='获取频道logo图片'
        api=self.yaml.get_PDDTapi(22)
        #获取数据
        channelid='10404'
        data={'channelid':channelid}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_019_assertinchannel(self):
        '''频道电台类-判断自己是否在特定频道内'''
        casename='判断自己是否在特定频道内'
        api=self.yaml.get_PDDTapi(23)
        sql='select * from channel;'
        #获取数据
        sqldata=self.db.get_selectdata_row(sql,0)
        token=sqldata[3]
        channelid=sqldata[1]
        data={'token':token,'channelid':channelid}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            #存在时反馈判断
            try:
                self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)\
                and self.assertEqual(result['result'],True)
                self.log.info('[%s]-[Result]:PASS'%casename)
                self.log.info('-'*60)
            #不存在时反馈判断
            except:
                self.assertEqual(result['errorCode'], 0) and self.assertEqual(result['isTrue'], True) \
                and self.assertEqual(result['result'], False)
                self.log.info('[%s]-[Result]:PASS' % casename)
                self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_020_allmember(self):
        '''频道电台类-取得和我相关的所有频道和频道成员列表(不包含自己)'''
        casename='取得和我相关的所有频道和频道成员列表(不包含自己)'
        api=self.yaml.get_PDDTapi(26)
        sql='select * from channel;'
        #获取数据
        token=self.db.get_specific_data(sql,0,3)
        data={'token':'234123414'}
        #发送请求
        try:
            result=self.req.get_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)\
            and self.assertEqual(result['errorMessage'],'操作成功')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-'*60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-'*60)
            raise

    def test_021_radionews(self):
        '''频道电台类-获取最新路况交通新闻'''
        casename='获取最新路况交通新闻'
        api=self.yaml.get_PDDTapi(27)
        sql='select * from channel;'
        #获取数据
        userid=self.db.get_specific_data(sql,0,2)
        data={'userid':userid}
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
