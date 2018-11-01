#!/user/bin/env python
#!encoding=utf-8
import unittest
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.YamlTools import YamlTools
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.CommonApiTools import CommonApiTools

'''数据采集类api接口测试'''

class API_SJCJ(unittest.TestCase):
    '''数据采集类api接口测试'''
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

    def test_001_position(self):
        '''数据采集类-提交用户位置信息'''
        casename='提交用户位置信息'
        api=self.yaml.get_SJCJapi(0)
        sql='select * from userlogin;'
        #获取数据信息
        userid=self.db.get_specific_data(sql,0,3)
        longitude='126.23435'       #经度
        latitude='31.4343'          #纬度
        body={'userid':userid,'longitude':longitude,'latitude':latitude}

        # 发送请求
        try:
            result=self.req.put_method(api,casename,body)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'信息更新成功')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-' * 60)
            raise

    def test_002_mobileinfo(self):
        '''数据采集类-提交用户手机信息'''
        casename='提交用户手机信息'
        api=self.yaml.get_SJCJapi(1)
        sql='select * from userlogin;'
        #获取数据信息
        phoneid=self.db.get_specific_data(sql,0,4)
        phonetype=0                                 #0：为ios，1：为android，2：为其它
        detail={'brand':'Iphone','version':'6','运营商':'中国电信','osversion':'ios12'}
        #配置参数
        body={'phoneid':phoneid,'phonetype':phonetype,'detail':detail}

        # 发送请求
        try:
            result=self.req.put_method(api,casename,body)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'信息更新成功')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
            raise

    def test_003_networkflow(self):
        '''数据采集类-提交用户使用流量信息'''
        casename='提交用户使用流量信息'
        api=self.yaml.get_SJCJapi(2)
        sql='select * from userlogin;'
        #获取数据信息--整行
        sqldata=self.db.get_selectdata_row(sql,0)
        #获取单个数据信息
        userid=sqldata[3]
        phoneid=sqldata[4]
        starttime='1487727617982'   #统计开始时间,单位：毫秒数
        endtime='1487727634678'     #统计截止时间,单位：毫秒数
        flow=34434388               #使用的3G/4G流量(不含WiFi)，单位：字节Byte
        navtime=2103                #导航功能实际使用时间(不含目的地搜索和路线规划时间)；单位：秒
        chattime=107                #使用对讲功能的时间(不含聊天机器人，不计算听别人说话的时间)；单位：秒
        usetime=5609                #使用嘟嘟的时间(app启动开始计算，切换或者关掉则停止计算)；单位：秒
        sharetimes=4                #分享图片的次数;单位：次数
        data={'userid':userid,'starttime':starttime,'endtime':endtime,'phoneid':phoneid,'flow':flow,
            'navtime':navtime,'chattime':chattime,'usetime':usetime,'sharetimes':sharetimes}
        # 发送请求
        try:
            result=self.req.post_method('json',api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True) and self.assertEqual(result['errorMessage'],'信息更新成功')
            self.log.info('[%s]-[Result]:PASS'%casename)
            self.log.info('-' * 60)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            self.log.info('-' * 60)
            raise


    def test_004_deletefile(self):
        '''数据采集类-用户删除上传到服务器的文件'''
        casename='用户删除上传到服务器的文件'
        api=self.yaml.get_SJCJapi(5)
        sql='select * from userlogin;'
        #获取数据
        userid=self.db.get_specific_data(sql,0,3)
        fileid='mro6vatc6fgflnrj54nqtixlyvn21r1r'
        data='userid=%s&fileid=%s'%(userid,fileid)
        # 发送请求
        try:
            result=self.req.delete_method(api,casename,data)
            self.assertEqual(result['errorCode'],0) and self.assertEqual(result['isTrue'],True)
            self.log.info('[%s]-[Result]:PASS'%casename)
        except Exception:
            self.log.error('[%s]-[Result]:FAILED'%casename)
            raise



if __name__=="__main__":
    unittest.main()