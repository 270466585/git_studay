#!/user/bin/env python
#!encoding=utf-8
import os
from Common.ExcelTools.ExcelReadTools import ExcelReadTools
from Common.ExcelTools.ExcelWriteTools import ExcelWriteTools
from Common.CommonTools.PathTools import data_path
from Common.CommonTools.RequestTools import RequestTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.DataBaseTools import DataBaseTools
'''
Excel数据驱动文件api测试
1、读取指定的excel文件中每个指定sheet中的接口信息
2、将接口信息配置成接口参数并配置发送请求类型
3、判断响应信息内容并给予PASS与FAIL结果
4、生成ExcelTest测试报告
5、统计每个sheet的测试结果，获取用例总数、成功总数、失败总数、跳过总数并计算通过率
6、将结果更新到封面
'''

class ExcelTestTools:
    def __init__(self,reportname=None):
        '''初始化'''
        datafile=os.path.join(data_path,'Data_API.xlsx')    #定位API数据文件
        self.readexcel=ExcelReadTools(datafile)
        self.writeexcel=ExcelWriteTools(reportname)
        self.req=RequestTools()
        self.log=LogTools()
        self.db=DataBaseTools()
        #统计测试用例数量信息
        self.sumnum=0           #用例总数
        self.successnum=0       #成功笔数
        self.failnum=0          #失败笔数

    def get_sheet_nrows(self,sheetname):
        '''
        获取sheet行数
        :param sheetname: 工作表sheet
        :return: 行数
        '''
        return self.readexcel.get_nrows(sheetname)

    def read_sheet(self,sheetname):
        '''
        读取指定sheet中的每行的数据信息并保存在字典中
        :param sheetname: sheet名称
        :return: 返回一个装有对应sheet的所有参数数据字典
        '''
        data_dict={}
        #获取指定sheet的行数
        getrows=self.get_sheet_nrows(sheetname)
        #获取每行的值
        for i in range(1,getrows):
            get_data=self.readexcel.get_row_values(sheetname,i)     #获取当行
            data_dict[i]=get_data                                   #行数:参数值
        return data_dict

    def get_param_dict(self,sheetname,key):
        '''
        获取data_dict中指定key对应的参数
        :param data_dict: 数据字典
        :param key: key值(1、2、3...)
        :return: 参数字典
        '''
        param_dict={}
        data_dict=self.read_sheet(sheetname)
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

    def send_request(self,param_dict,worksheet,cellid):
        '''
        根据参数字典发送请求
        :param param_dict : 参数字典
        :param worksheet : 工作sheet
        '''
        #统计用例总数
        self.sumnum+=1
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

        #设定单元格样式
        body_format=self.writeexcel.set_cellformat(font_size=10)

        #判断发送类型并调用请求函数
        #get请求
        if request_type=='get':
            #发送请求
            try:
                result=self.req.get_method(api,test_title,url_param)
                if result['errorCode']==errorCode and result['isTrue']==isTrue and result['errorMessage']==errorMessage:
                    self.log.info('[%s]-[Result]:PASS'%test_title)
                    self.log.info('-'*60)
                    #插入相关结果到excel表
                    self.writeexcel.write_cell(worksheet,'I%d'%cellid,str(result),body_format)                   #响应信息
                    self.writeexcel.write_cell(worksheet,'K%d'%cellid,result['errorCode'],body_format)      #实际errorCode
                    self.writeexcel.write_cell(worksheet,'M%d'%cellid,result['isTrue'],body_format)         #实际isTrue
                    self.writeexcel.write_cell(worksheet,'O%d'%cellid,result['errorMessage'],body_format)   #实际errorMessage
                    self.writeexcel.write_pass(worksheet,'P%d'%cellid)      #PASS
                    self.successnum+=1      #记录成功用例个数
                else:
                    self.log.error('[%s]-[Result]:FAILED' % test_title)
                    self.log.info('-' * 60)
                    # 插入相关结果到excel表
                    self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)              #响应信息
                    self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                    self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)    # 实际isTrue
                    self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                    self.writeexcel.write_fail(worksheet, 'P%d' % cellid)  # FAIL
                    self.failnum+=1         #记录失败用例个数
            except Exception as e:
                self.writeexcel.write_na(worksheet,'P%d'%cellid)    #N/A
                self.log.error('[%s]-[Error]:%s'%(test_title,e))
        #put请求
        elif request_type=='put':
            #发送请求
            try:
                result=self.req.put_method(api,test_title,data_param,url_param)
                if result['errorCode']==errorCode and result['isTrue']==isTrue and result['errorMessage']==errorMessage:
                    self.log.info('[%s]-[Result]:PASS' % test_title)
                    self.log.info('-' * 60)
                    # 插入相关结果到excel表
                    self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                    self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                    self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                    self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                    self.writeexcel.write_pass(worksheet, 'P%d' % cellid)  # PASS
                    self.successnum+=1
                else:
                    self.log.error('[%s]-[Result]:FAILED' % test_title)
                    self.log.info('-' * 60)
                    # 插入相关结果到excel表
                    self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                    self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                    self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                    self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                    self.writeexcel.write_fail(worksheet, 'P%d' % cellid)  # FAIL
                    self.failnum+=1
            except Exception as e:
                self.writeexcel.write_na(worksheet, 'P%d' % cellid)  # N/A
                self.log.error('[%s]-[Error]:%s'%(test_title,e))
        #delete请求
        elif request_type=='delete':
            #发送请求
            try:
                result=self.req.delete_method(api,test_title,url_param)
                if result['errorCode']==errorCode and result['isTrue']==isTrue and result['errorMessage']==errorMessage:
                    self.log.info('[%s]-[Result]:PASS' % test_title)
                    self.log.info('-' * 60)
                    # 插入相关结果到excel表
                    self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                    self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                    self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                    self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                    self.writeexcel.write_pass(worksheet, 'P%d' % cellid)  # PASS
                    self.successnum+=1
                else:
                    self.log.error('[%s]-[Result]:FAILED' % test_title)
                    self.log.info('-' * 60)
                    # 插入相关结果到excel表
                    self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                    self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                    self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                    self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                    self.writeexcel.write_fail(worksheet, 'P%d' % cellid)  # FAIL
                    self.failnum+=1
            except Exception as e:
                self.writeexcel.write_na(worksheet, 'P%d' % cellid)  # N/A
                self.log.error('[%s]-[Error]:%s'%(test_title,e))
        #post请求
        elif request_type=='post':
            # post类型为urlencode
            if post_type=='urlencode':
                try:
                    result=self.req.post_method('urlencode',api,test_title,data_param,url_param)
                    if result['errorCode'] == errorCode and result['isTrue'] == isTrue and result[
                        'errorMessage'] == errorMessage:
                        self.log.info('[%s]-[Result]:PASS' % test_title)
                        self.log.info('-' * 60)
                        # 插入相关结果到excel表
                        self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                        self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                        self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                        self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                        self.writeexcel.write_pass(worksheet, 'P%d' % cellid)  # PASS
                        self.successnum+=1
                    else:
                        self.log.error('[%s]-[Result]:FAILED' % test_title)
                        self.log.info('-' * 60)
                        # 插入相关结果到excel表
                        self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                        self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                        self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                        self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                        self.writeexcel.write_fail(worksheet, 'P%d' % cellid)  # FAIL
                        self.failnum+=1
                except Exception as e:
                    self.writeexcel.write_na(worksheet, 'P%d' % cellid)  # N/A
                    self.log.error('[%s]-[Error]:%s' % (test_title, e))
            # post类型为form
            elif post_type=='form':
                try:
                    result=self.req.post_method('form',api,test_title,data_param,url_param)
                    if result['errorCode'] == errorCode and result['isTrue'] == isTrue and result[
                        'errorMessage'] == errorMessage:
                        self.log.info('[%s]-[Result]:PASS' % test_title)
                        self.log.info('-' * 60)
                        # 插入相关结果到excel表
                        self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                        self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                        self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                        self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                        self.writeexcel.write_pass(worksheet, 'P%d' % cellid)  # PASS
                        self.successnum+=1
                    else:
                        self.log.error('[%s]-[Result]:FAILED' % test_title)
                        self.log.info('-' * 60)
                        # 插入相关结果到excel表
                        self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                        self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                        self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                        self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                        self.writeexcel.write_fail(worksheet, 'P%d' % cellid)  # FAIL
                        self.failnum+=1
                except Exception as e:
                    self.writeexcel.write_na(worksheet, 'P%d' % cellid)  # N/A
                    self.log.error('[%s]-[Error]:%s' % (test_title, e))
            # post类型为json
            elif post_type=='json':
                try:
                    result=self.req.post_method('json',api,test_title,data_param,url_param)
                    if result['errorCode'] == errorCode and result['isTrue'] == isTrue and result[
                        'errorMessage'] == errorMessage:
                        self.log.info('[%s]-[Result]:PASS' % test_title)
                        self.log.info('-' * 60)
                        # 插入相关结果到excel表
                        self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                        self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                        self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                        self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                        self.writeexcel.write_pass(worksheet, 'P%d' % cellid)  # PASS
                        self.successnum+=1
                    else:
                        self.log.error('[%s]-[Result]:FAILED' % test_title)
                        self.log.info('-' * 60)
                        # 插入相关结果到excel表
                        self.writeexcel.write_cell(worksheet, 'I%d' % cellid, str(result), body_format)  # 响应信息
                        self.writeexcel.write_cell(worksheet, 'K%d' % cellid, result['errorCode'],body_format)  # 实际errorCode
                        self.writeexcel.write_cell(worksheet, 'M%d' % cellid, result['isTrue'], body_format)  # 实际isTrue
                        self.writeexcel.write_cell(worksheet, 'O%d' % cellid, result['errorMessage'],body_format)  # 实际errorMessage
                        self.writeexcel.write_fail(worksheet, 'P%d' % cellid)  # FAIL
                        self.failnum+=1
                except Exception as e:
                    self.writeexcel.write_na(worksheet, 'P%d' % cellid)  # N/A
                    self.log.error('[%s]-[Error]:%s' % (test_title, e))
            else:
                print('POST请求类型设置错误！')
        else:
            print('无对应请求的封装函数，请核实！')

    def write_cover_info(self,worksheet,title,sumnum,successnum,failnum,skipnum,usetime):
        '''
        构造封面
        :param title: 封面主题
        :param sumnum: 用例总数
        :param successnum: 成功用例数量
        :param failnum: 失败用例数量
        :param skipnum: 跳过用例数量
        :param usetime: 执行时间
        '''
        self.writeexcel.create_cover_gui(worksheet,title,sumnum,successnum,failnum,skipnum,usetime)

    def write_basic_info(self,sheetname):
        '''
        将基本信息写入到指定的sheet中
        :param sheetname: 工作表名称
        '''
        data_list=[]
        #读取对应sheet的所有数据信息
        sumrows=self.readexcel.get_nrows(sheetname)
        #循环获取每行的数据（字典类型），然后存放于列表中
        for i in range(1,sumrows):
            param_dict=self.get_param_dict(sheetname,i)
            data_list.append(param_dict)
        #创建sheet
        self.sheet=self.writeexcel.add_worksheet(sheetname)
        #写入基础信息框架
        self.writeexcel.create_table_gui(self.sheet)
        #设定单元格样式
        body_format=self.writeexcel.set_cellformat(font_size=10)
        #循环写入信息
        for k in range(1,len(data_list)+1):
            self.writeexcel.write_cell(self.sheet,'A%d'%(k+1),k,body_format)     #用例ID
            self.writeexcel.write_cell(self.sheet,'B%d'%(k+1),data_list[k-1]['test_class'],body_format)      #模块名称
            self.writeexcel.write_cell(self.sheet,'C%d'%(k+1),data_list[k-1]['test_title'],body_format)      #用例内容
            self.writeexcel.write_cell(self.sheet,'D%d'%(k+1),data_list[k-1]['api'],body_format)             #URL
            self.writeexcel.write_cell(self.sheet,'E%d'%(k+1),data_list[k-1]['request_type'],body_format)    #请求方式
            self.writeexcel.write_cell(self.sheet,'F%d'%(k+1),data_list[k-1]['headers'],body_format)         #headers
            self.writeexcel.write_cell(self.sheet,'G%d'%(k+1),data_list[k-1]['url_param'],body_format)       #url参数
            self.writeexcel.write_cell(self.sheet,'H%d'%(k+1),data_list[k-1]['data_param'],body_format)      #data参数
            self.writeexcel.write_cell(self.sheet,'J%d'%(k+1),data_list[k-1]['errorCode'],body_format)       #预期errorCode
            self.writeexcel.write_cell(self.sheet,'L%d'%(k+1),data_list[k-1]['isTrue'],body_format)          #预期isTrue
            self.writeexcel.write_cell(self.sheet,'N%d'%(k+1),data_list[k-1]['errorMessage'],body_format)    #预期errorMessage
        return self.sheet

    def do_excel_alltests(self,sheetname):
        '''
        执行excel所有的测试用例，步骤如下：
        1、通过sheetname参数去默认的路径下生成ExcelReport文件，并构建sheet框架
        2、通过sheetname参数去数据驱动Data_API.xlsx文件中找到对应的sheet并获取总行数
        3、根据总行数循环获取Data_API.xlsx对应sheet的数据，对每行数据进行数据重组为param_dict
        4、send_request对param_dict的数据进行抓取，同时组合接口请求参数发起接口请求（判断请求类型）
        5、send_request对返回值与excel表的预期值进行对比，对比通过则pass，不通过则fail
        6、send_request将返回值中的相关要素插入到ExcelReport中对应的sheet中
        :param sheetname: 工作表名称
        :return:返回sumnum总执行用例、successnum成功用例、failnum失败用例
        '''
        try:
            sheet=self.write_basic_info(sheetname)
            nrows=self.get_sheet_nrows(sheetname)
            for i in range(1, nrows):
                param_dict = self.get_param_dict(sheetname,i)
                self.send_request(param_dict,sheet,i+1)
            #保存数据
            num_dict={}
            num_dict['sumnum']=self.sumnum
            num_dict['successnum']=self.successnum
            num_dict['failnum']=self.failnum
            #初始化数据
            self.sumnum=0
            self.successnum=0
            self.failnum=0
            return num_dict
        except Exception:
            print('执行失败，请检查sheetname是否在Data_API.xlsx中存在.')
            raise


    def closeTools(self):
        '''关闭ExcelWriter'''
        self.writeexcel.close_workbook()

if __name__=="__main__":
    excel=ExcelTestTools()
    sumnum,successnum,failnum=excel.do_excel_alltests('ZC')
    print(sumnum,successnum,failnum)
    excel.closeTools()


