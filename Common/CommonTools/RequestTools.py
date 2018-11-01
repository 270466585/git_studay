#!/user/bin/env python
#!encoding=utf-8
import json
import requests
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.PathTools import config_path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from Common.CommonTools.ConfigReadTools import ConfigReadTools

'''封装请求发送函数'''

class RequestTools:
    def __init__(self):
        '''读取配置文件,将内容转换为字典形式'''
        # 关闭安全请求警告
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.readconf=ConfigReadTools(config_path)
        #获取host数据
        self.host=self.readconf.get_section_item('HOST_CONF')
        #获取请求头
        self.headers =self.readconf.get_section_item('HEADER_CONF')
        #获取状态错误码
        self.status_errorcode =self.readconf.get_section_item('RES_ERROR_CODE')
        #获取验证状态
        self.verify=self.headers['Verify']
        #判断http/https，修改验证verify状态
        if self.host['Scheme']=='https':
            self.verify=False
        else:
            self.verify=True
        self.readconf.conf_save()
        #创建一个session
        self.req=requests.session()
        #创建日志
        self.log=LogTools()


    def get_method(self,api,apiname,data=None):
        '''
        发送GET请求
        :param api:api地址
        :param apiname:api名称
        :param data: get请求参数
        :return: 相关返回信息
        '''
        try:
            url='%s://%s%s'%(self.host['Scheme'],self.host['Url'],api)
            req=self.req.get(url=url,params=data,headers=self.headers,verify=self.verify)
            #若返回状态为200
            if req.status_code==200:
                result_json = req.json()  # 返回json文本
                result_url = req.url  # 返回url地址
                result_status=req.status_code
                #日志输出相关请求要素
                self.log.info('[%s]-[URL]:%s' % (apiname, result_url))
                self.log.info('[%s]-[StautsCode]:%s'%(apiname,result_status))
                self.log.info('[%s]-[Headers]:%s'%(apiname,self.headers))
                self.log.info('[%s]-[Parameter]:%s' % (apiname, data))
                self.log.info('[%s]-[Return_value]:%s' % (apiname, result_json))
                return result_json

            #若返回错误状态为配置错误码
            elif str(req.status_code) in self.status_errorcode.keys():
                self.log.error('[%s]-[StatusCode]:[%s]-%s'%(apiname,req.status_code,self.status_errorcode.get(str(req.status_code))))

            #若返回错误状态不在配置错误码
            elif str(req.status_code) not in self.status_errorcode.keys():
                self.log.error('[%s]-[StatusCode]:[%s]-其他错误返回码' % (apiname,req.status_code))
        except Exception as e:
            #系统报错
            self.log.error('[%s]-[UnknownError]:%s' %(apiname,e))

    def post_method(self,method,api,apiname,data,body=None):
        '''
        发送POST请求
        :param method:POST发送请求类型
        :param api: api地址
        :param apiname:api名称
        :param data: post请求参数
        :return: 返回响应信息
        '''
        if method=='urlencode':
            return self._post_method_urlencode(api,apiname,data,body)
        elif method=='form':
            return self._post_method_form(api,apiname,data)
        elif method=='json':
            return self._post_method_json(api,apiname,data)
        else:
            print('POST请求类型选择有误.')


    def _post_method_urlencode(self,api,apiname,data,body=None):
        '''
        发送Post请求（类型为urlencode）
        :param api: api地址
        :param apiname:api名称
        :param data: post参数（参数1=参数值1&参数2=参数值2&参数3=参数值3）
        :param body: post参数（写在body中）
        :return: post请求返回信息
        '''
        try:
            url='%s://%s%s?%s'%(self.host['Scheme'],self.host['Url'],api,data)
            req=requests.post(url=url,headers=self.headers,verify=self.verify,data=body)
            #状态为200
            if req.status_code==200:
                result_json = req.json()            # 返回json文本
                result_url = req.url                # 返回url地址
                result_status=req.status_code       # 返回状态码
                # 日志输出相关请求要素
                self.log.info('[%s]-[URL]:%s' % (apiname, result_url))
                self.log.info('[%s]-[StautsCode]:%s' % (apiname, result_status))
                self.log.info('[%s]-[Headers]:%s' % (apiname, self.headers))
                self.log.info('[%s]-[Parameter]:%s' % (apiname, data))
                self.log.info('[%s]-[Body]:%s'%(apiname,body))
                self.log.info('[%s]-[Return_value]:%s' % (apiname, result_json))
                return result_json
            #状态为配置错误码
            elif str(req.status_code) in self.status_errorcode.keys():
                self.log.error('[%d]:%s' % (req.status_code, self.status_errorcode.get(str(req.status_code))))
            # 若返回错误状态不在配置错误码
            elif str(req.status_code) not in self.status_errorcode.keys():
                self.log.error('[%d]:其他错误返回码' % (req.status_code))
        except Exception as e:
            #系统报错
            self.log.error('[系统错误]:%s' % e)

    def _post_method_form(self,api,apiname,data):
        '''
        发送post请求（类型为form）
        :param api: api地址
        :param apiname:api名称
        :param data: post参数
        :return: post请求返回信息
        '''
        try:
            url='%s://%s%s'%(self.host['Scheme'],self.host['Url'],api)
            req=self.req.post(url=url,headers=self.headers,data=data,verify=self.verify)
            # 状态为200
            if req.status_code == 200:
                result_json = req.json()            # 返回json文本
                result_status = req.status_code     # 返回状态码
                result_url = req.url                # 返回url地址
                # 日志输出相关请求要素
                self.log.info('[%s]-[URL]:%s' % (apiname, result_url))
                self.log.info('[%s]-[StautsCode]:%s' % (apiname, result_status))
                self.log.info('[%s]-[Headers]:%s' % (apiname, self.headers))
                self.log.info('[%s]-[Parameter]:%s' % (apiname, data))
                self.log.info('[%s]-[Return_value]:%s' % (apiname, result_json))
                return result_json
            # 状态为配置错误码
            elif str(req.status_code) in self.status_errorcode.keys():
                self.log.error('[%d]:%s' % (req.status_code, self.status_errorcode.get(str(req.status_code))))
            # 若返回错误状态不在配置错误码
            elif str(req.status_code) not in self.status_errorcode.keys():
                self.log.error('[%d]:其他错误返回码' % (req.status_code))
        except Exception as e:
            # 系统报错
            self.log.error('[系统错误]:%s' % e)

    def _post_method_json(self,api,apiname,data):
        '''
        发送post请求（类型为json）
        :param api: api地址
        :param apiname:api名称
        :param data: post参数
        :return: post请求返回信息
        '''
        try:
            url='%s://%s%s'%(self.host['Scheme'],self.host['Url'],api)
            req=self.req.post(url=url,headers=self.headers,json=data,verify=self.verify)
            # 状态为200
            if req.status_code == 200:
                result_json = req.json()            # 返回json文本
                result_status = req.status_code     # 返回状态码
                result_url = req.url                # 返回url地址
                # 日志输出相关请求要素
                self.log.info('[%s]-[URL]:%s' % (apiname, result_url))
                self.log.info('[%s]-[StautsCode]:%s' % (apiname, result_status))
                self.log.info('[%s]-[Headers]:%s' % (apiname, self.headers))
                self.log.info('[%s]-[Parameter]:%s' % (apiname, data))
                self.log.info('[%s]-[Return_value]:%s' % (apiname, result_json))
                return result_json

            # 状态为配置错误码
            elif str(req.status_code) in self.status_errorcode.keys():
                self.log.error('[%d]:%s' % (req.status_code, self.status_errorcode.get(str(req.status_code))))
            # 若返回错误状态不在配置错误码
            elif str(req.status_code) not in self.status_errorcode.keys():
                self.log.error('[%d]:其他错误返回码' % (req.status_code))
        except Exception as e:
            # 系统报错
            self.log.error('[系统错误]:%s' % e)

    def put_method(self,api,apiname,body=None,data=None):
        '''
        发送put请求
        :param api: api地址
        :param apiname: api名称
        :param body: body参数
        :param data: put参数
        '''
        try:
            if data!=None:
                url='%s://%s%s?%s'%(self.host['Scheme'],self.host['Url'],api,data)
            else:
                url='%s://%s%s'%(self.host['Scheme'],self.host['Url'],api)
            req=self.req.put(url=url,headers=self.headers,json=body,verify=self.verify)
            # 状态为200
            if req.status_code == 200:
                result_json = req.json()  # 返回json文本
                result_status = req.status_code  # 返回状态码
                result_url = req.url  # 返回url地址
                # 日志输出相关请求要素
                self.log.info('[%s]-[URL]:%s' % (apiname, result_url))
                self.log.info('[%s]-[StautsCode]:%s' % (apiname, result_status))
                self.log.info('[%s]-[Headers]:%s' % (apiname, self.headers))
                self.log.info('[%s]-[BodyParameter]:%s' % (apiname, body))
                self.log.info('[%s]-[DataParameter]:%s'% (apiname,data))
                self.log.info('[%s]-[Return_value]:%s' % (apiname, result_json))
                return result_json

            # 状态为配置错误码
            elif str(req.status_code) in self.status_errorcode.keys():
                self.log.error('[%d]:%s' % (req.status_code, self.status_errorcode.get(str(req.status_code))))
            # 若返回错误状态不在配置错误码
            elif str(req.status_code) not in self.status_errorcode.keys():
                self.log.error('[%d]:其他错误返回码' % (req.status_code))
        except Exception as e:
            # 系统报错
            self.log.error('[系统错误]:%s' % e)

    def delete_method(self,api,apiname,data=None,body=None):
        '''
        delete请求方法
        :param api: api地址
        :param apiname: api接口名称
        :param data: delete参数
        '''
        try:
            if data!=None:
                url='%s://%s%s?%s'%(self.host['Scheme'],self.host['Url'],api,data)
            else:
                url='%s://%s%s'%(self.host['Scheme'],self.host['Url'],api)
            req=self.req.delete(url=url,headers=self.headers,verify=self.verify,json=body)
            # 状态为200
            if req.status_code == 200:
                result_json = req.json()  # 返回json文本
                result_status = req.status_code  # 返回状态码
                result_url = req.url  # 返回url地址
                # 日志输出相关请求要素
                self.log.info('[%s]-[URL]:%s' % (apiname, result_url))
                self.log.info('[%s]-[StautsCode]:%s' % (apiname, result_status))
                self.log.info('[%s]-[Headers]:%s' % (apiname, self.headers))
                self.log.info('[%s]-[BodyParameter]:%s' % (apiname, body))
                self.log.info('[%s]-[DataParameter]:%s' % (apiname, data))
                self.log.info('[%s]-[Return_value]:%s' % (apiname, result_json))
                return result_json

            # 状态为配置错误码
            elif str(req.status_code) in self.status_errorcode.keys():
                self.log.error('[%d]:%s' % (req.status_code, self.status_errorcode.get(str(req.status_code))))
            # 若返回错误状态不在配置错误码
            elif str(req.status_code) not in self.status_errorcode.keys():
                self.log.error('[%d]:其他错误返回码' % (req.status_code))
        except Exception as e:
            # 系统报错
            self.log.error('[系统错误]:%s' % e)


if __name__=="__main__":
    request=RequestTools()
    # print(request.get_method('/WebAPI/rest/sys/time'))
    # data={"userid" : "user10234","username" : "AppoloLi","mobile" : "13921342314","password" : "","validcode" : "123456"}
    # print(request.post_method('urlencode','/WebAPI/rest/register',data))
