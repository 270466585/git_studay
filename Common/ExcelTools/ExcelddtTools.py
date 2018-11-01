#!/user/bin/env python
#!encoding=utf-8
import os
from Common.ExcelTools.ExcelReadTools import ExcelReadTools
from Common.CommonTools.PathTools import data_path
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.DataBaseTools import DataBaseTools

'''Excelddt数据驱动unittest测试相关函数'''

class ExcelDDTTools:
    def __init__(self):
        '''初始化'''
        datafile = os.path.join(data_path, 'Data_API.xlsx')  # 定位数据文件
        self.readexcel = ExcelReadTools(datafile)
        self.req = RequestTools()
        self.log = LogTools()
        self.db = DataBaseTools()

    def get_ddt_datalist(self,sheetname):
        '''
        获取指定sheet内的所有数据，并组合成ddt_data列表
        :param sheetname: sheet表
        :return: ddt_datalist
        '''
        ddt_datalist=[]
        nrows=self.readexcel.get_nrows(sheetname)
        for i in range(1,nrows):
            param_dict=self._get_param_dict(sheetname,i)
            ddt_datalist.append(param_dict)
        return ddt_datalist

    def _read_sheet(self,sheetname):
        '''
        读取指定sheet中的每行的数据信息并保存在字典中
        :param sheetname: sheet名称
        :return: 返回一个装有对应sheet的所有参数数据字典
        '''
        data_dict={}
        #获取指定sheet的行数
        getrows=self.readexcel.get_nrows(sheetname)
        #获取每行的值
        for i in range(1,getrows):
            get_data=self.readexcel.get_row_values(sheetname,i)     #获取当行
            data_dict[i]=get_data                                   #行数:参数值
        return data_dict

    def _get_param_dict(self,sheetname,key):
        '''
        获取data_dict中指定key对应的参数
        :param data_dict: 数据字典
        :param key: key值(1、2、3...)
        :return: 参数字典
        '''
        param_dict={}
        data_dict=self._read_sheet(sheetname)
        param_list=data_dict[key]
        #获取token值
        sql='select token from userlogin where telnum=17318971827;'
        token=self.db.get_selectdata_row(sql,0)
        #获取参数组合成字典
        param_dict['test_class']=param_list[0]
        param_dict['test_title']=param_list[1]
        param_dict['api']=param_list[2]
        param_dict['request_type']=param_list[3]
        param_dict['post_type']=param_list[4]
        param_dict['url_param']=param_list[5]
        param_dict['data_param']=param_list[6]
        param_dict['headers']=param_list[7]
        param_dict['errorCode']=param_list[8]
        param_dict['isTrue']=param_list[9]
        param_dict['errorMessage']=param_list[10]
        param_dict['token']=token[0]
        return param_dict

    def send_request(self,param_dict):
        '''
        根据参数字典发送请求
        :param param_dict : 参数字典
        :param worksheet : 工作sheet
        '''
        #获取参数字典各类参数值
        test_class=param_dict['test_class']
        test_title=param_dict['test_title']
        api=param_dict['api']
        request_type=param_dict['request_type']
        post_type=param_dict['post_type']
        url_param=param_dict['url_param']
        data_param=param_dict['data_param']
        headers=param_dict['headers']
        errorCode=param_dict['errorCode']
        isTrue=param_dict['isTrue']
        errorMessage=param_dict['errorMessage']

        #转换url_param参数
        if url_param=='':
            url_param=None
        elif '=' in url_param:
            url_param=url_param
        else:
            url_param=eval(url_param)
        #转换data_param参数
        if data_param=='':
            data_param=None
        else:
            data_param=eval(data_param)
        #转换errorCode'
        errorCode=int(errorCode)
        #转换isTrue参数
        if isTrue == 'True':
            isTrue = True
        elif isTrue == 'False':
            isTrue = False

        #判断发送类型并调用请求函数
        #get请求
        if request_type=='get':
            #发送请求
            try:
                result=self.req.get_method(api,test_title,url_param)
                #返回数据判断
                assert result['errorCode']==errorCode
                assert result['isTrue']==isTrue
                assert result['errorMessage']==errorMessage
                self.log.info('[%s]-[Result]:PASS'%test_title)
                self.log.info('-'*60)
            except Exception:
                self.log.error('[%s]-[Result]:FAILED' % test_title)
                self.log.info('-' * 60)
                raise
        #put请求
        elif request_type=='put':
            #发送请求
            try:
                result=self.req.put_method(api,test_title,data_param,url_param)
                # 返回数据判断
                assert result['errorCode'] == errorCode
                assert result['isTrue'] == isTrue
                assert result['errorMessage'] == errorMessage
                self.log.info('[%s]-[Result]:PASS' % test_title)
                self.log.info('-' * 60)
            except Exception:
                self.log.error('[%s]-[Result]:FAILED' % test_title)
                self.log.info('-' * 60)
                raise
        #delete请求
        elif request_type=='delete':
            #发送请求
            try:
                result=self.req.delete_method(api,test_title,url_param)
                # 返回数据判断
                assert result['errorCode'] == errorCode
                assert result['isTrue'] == isTrue
                assert result['errorMessage'] == errorMessage
                self.log.info('[%s]-[Result]:PASS' % test_title)
                self.log.info('-' * 60)
            except Exception:
                self.log.error('[%s]-[Result]:FAILED' % test_title)
                self.log.info('-' * 60)
                raise
        #post请求
        elif request_type=='post':
            # post类型为urlencode
            if post_type=='urlencode':
                try:
                    result=self.req.post_method('urlencode',api,test_title,data_param,url_param)
                    #返回数据判断
                    assert result['errorCode'] == errorCode
                    assert result['isTrue'] == isTrue
                    assert result['errorMessage'] == errorMessage
                    self.log.info('[%s]-[Result]:PASS' % test_title)
                    self.log.info('-' * 60)
                except Exception:
                    self.log.error('[%s]-[Result]:FAILED' % test_title)
                    self.log.info('-' * 60)
                    raise
            # post类型为form
            elif post_type=='form':
                try:
                    result=self.req.post_method('form',api,test_title,data_param,url_param)
                    # 返回数据判断
                    assert result['errorCode'] == errorCode
                    assert result['isTrue'] == isTrue
                    assert result['errorMessage'] == errorMessage
                    self.log.info('[%s]-[Result]:PASS' % test_title)
                    self.log.info('-' * 60)
                except Exception:
                    self.log.error('[%s]-[Result]:FAILED' % test_title)
                    self.log.info('-' * 60)
                    raise
            # post类型为json
            elif post_type=='json':
                try:
                    result=self.req.post_method('json',api,test_title,data_param,url_param)
                    # 返回数据判断
                    assert result['errorCode'] == errorCode
                    assert result['isTrue'] == isTrue
                    assert result['errorMessage'] == errorMessage
                    self.log.info('[%s]-[Result]:PASS' % test_title)
                    self.log.info('-' * 60)
                except Exception:
                    self.log.error('[%s]-[Result]:FAILED' % test_title)
                    self.log.info('-' * 60)
                    raise
            else:
                print('POST请求类型设置错误！')

if __name__=="__main__":
    excel=ExcelDDTTools()
    ddt_list=excel.get_ddt_datalist('ZC')
    print(ddt_list)