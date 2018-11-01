#!/user/bin/env python
#!encoding=utf-8
import requests
from Common.CommonTools.DataBaseTools import DataBaseTools
from Common.CommonTools.ConfigReadTools import ConfigReadTools
from Common.CommonTools.PathTools import config_path
from requests.packages.urllib3.exceptions import InsecureRequestWarning

'''封装常用的api接口请求（登陆请求和退出请求）'''

class CommonApiTools:
    def __init__(self):
        # 关闭安全请求警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.configread=ConfigReadTools(config_path)
        self.db=DataBaseTools()
        self.loginapi_pwd='https://api.linkofcar.com/WebAPI/rest/auth/authorize'
        self.loginapi_verifycode='https://api.linkofcar.com/WebAPI/rest/auth/validcode'
        self.logoutapi='https://api.linkofcar.com/WebAPI/rest/auth/logout'
        self.loginverifycode_api='https://api.linkofcar.com/WebAPI/rest/register/sms'
        self.headers=self.configread.get_section_item('HEADER_CONF')
        self.verify=False

    def login_api_pwd(self):
        '''登陆接口(密码验证)'''
        sql1='select * from userlogin;'
        #获取数据库数据
        zcuid=self.db.get_specific_data(sql1,0,2)
        mobile=self.db.get_specific_data(sql1,0,0)
        password = self.db.get_specific_data(sql1,0,1)
        phoneid = self.db.get_specific_data(sql1,0,4)
        data={'userid':zcuid,'mobile':mobile,'pwd':password,'phoneid':phoneid}
        req=requests.get(url=self.loginapi_pwd,headers=self.headers,params=data,verify=self.verify)
        result=req.json()
        # 更新数据库信息--用户领驭号、token、登陆标志
        sql2 = 'update userlogin set dlbz=1,userid=\'%s\',token=\'%s\' where phoneid=\'%s\';' \
        % (result['result']['userid'], result['result']['token'], phoneid)
        self.db.execute_sql(sql2)


    def login_api_verifycode(self):
        '''登陆接口(验证码登陆)'''
        sql1='select * from userlogin;'
        #先申请登录验证码
        self.get_verifycode(0)
        #获取数据库数据
        telnum = self.db.get_specific_data(sql1, 0, 0)
        loginverifycode = self.db.get_specific_data(sql1, 0, 7)
        phoneid = self.db.get_specific_data(sql1, 0, 4)
        data = {'mobile': telnum, 'validcode': loginverifycode, 'phoneid': phoneid}
        req=requests.get(url=self.loginapi_verifycode,headers=self.headers,params=data,verify=self.verify)
        result=req.json()
        # 更新数据库信息--用户领驭号、token、登陆标志
        sql2 = 'update userlogin set dlbz=1,userid=\'%s\',token=\'%s\' where phoneid=\'%s\';' \
               % (result['result']['userid'], result['result']['token'], phoneid)
        self.db.execute_sql(sql2)



    def get_verifycode(self,type):
        '''
        获取验证码，type为1为注册验证码，type为0为登录验证码
        :param type:0-登录验证码，1-注册验证码
        '''
        sql1='select * from userlogin;'
        sql2='select * from verifycode;'
        #获取数据库数据
        telnum1=self.db.get_specific_data(sql1,0,0)      #已经注册的手机号码
        telnum2=self.db.get_specific_data(sql2,1,0)      #未注册的手机号码

        #注册验证码
        if type==1:
            data={'mobile':telnum2,'isregister':1}
            req=requests.get(url=self.loginverifycode_api,headers=self.headers,params=data,verify=self.verify)
            result=req.json()
            #更新数据库信息--注册验证码
            sql2='update verifycode set verifycode=\'%s\' where telnum=\'%s\';'%(result['result'],telnum2)
            self.db.execute_sql(sql2)

        #登陆验证码
        elif type==0:
            data={'mobile':telnum1,'isregister':0}
            req = requests.get(url=self.loginverifycode_api, headers=self.headers, params=data, verify=self.verify)
            result = req.json()
            #更新数据库信息--登陆验证码
            sql3='update userlogin set loginverifycode=\'%s\' where telnum=\'%s\';'%(result['result'],telnum1)
            self.db.execute_sql(sql3)


    def logout_api(self):
        '''注销退出接口(urlencode)'''
        sql1='select * from userlogin;'
        #获取userid
        userid=self.db.get_specific_data(sql1,0,3)
        url=self.logoutapi+'?'+'userid=%s'%userid
        try:
            req=requests.post(url=url,headers=self.headers,verify=self.verify)
            result=req.json()
            if result['errorCode']==0 and result['isTrue']==True:
                pass
            #更新登陆状态标志
            sql2='update userlogin set dlbz=0 where userid=\'%s\';'%userid
            self.db.execute_sql(sql2)
        except Exception as e:
            print('注销退出错误，具体错误:%s'%e)

if __name__=="__main__":
    common=CommonApiTools()
    common.logout_api()