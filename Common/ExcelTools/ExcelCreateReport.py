#!/user/bin/env python
#!encoding=utf-8
import datetime
from Common.ExcelTools.ExcelTestTools import ExcelTestTools
from Common.CommonTools.PathTools import execlreport_path

'''excel测试用例全量测试并生成ExcelReport'''

class ExcelCreateReport:
    def __init__(self):
        self.exceltest=ExcelTestTools()

    def create_report(self,title):
        '''
        执行内定excel文件所有api测试用例，生成测试报告
        :param title: 测试报告主题
        :return: 执行excel所有用例，生成测试报告，统计用例执行总数、用例成功笔数、
                 失败笔数、跳过笔数、执行时间、计算通过率，并构建饼图以及装饰封面
        '''
        cover=self.exceltest.writeexcel.add_worksheet('报告概况')    #创建封面sheet
        start_time=datetime.datetime.now()                     #计算测试开始时间
        #执行测试并获取总用例数量、成功用例数量、失败用例数量
        getnum_list=[]
        zc_num_dict=self.exceltest.do_excel_alltests('ZC')       #用户注册类
        hd_num_dict=self.exceltest.do_excel_alltests('HDGGYY')   #活动广告运营类
        tc_num_dict=self.exceltest.do_excel_alltests('TC')       #退出注销类
        xp_num_dict=self.exceltest.do_excel_alltests('XTPZ')     #系统配置类
        dl_num_dict=self.exceltest.do_excel_alltests('DL')       #登录类
        sj_num_dict=self.exceltest.do_excel_alltests('SJCJ')     #数据收集类
        hy_num_dict=self.exceltest.do_excel_alltests('HY')       #好友类
        pd_num_dict=self.exceltest.do_excel_alltests('PDDT')     #频道电台类

        # 计算结束时间并统计用例执行时间
        end_time = datetime.datetime.now()
        test_time = (end_time - start_time).total_seconds()

        #将数据加载到列表中
        getnum_list.append(zc_num_dict)
        getnum_list.append(hd_num_dict)
        getnum_list.append(tc_num_dict)
        getnum_list.append(xp_num_dict)
        getnum_list.append(dl_num_dict)
        getnum_list.append(sj_num_dict)
        getnum_list.append(hy_num_dict)
        getnum_list.append(pd_num_dict)

        # 统计整个测试报告总用例数、成功用例数、失败用例数、跳过用例数
        total_sumnum=0
        total_successnum=0
        total_failnum=0
        for i in getnum_list:
            total_sumnum += i['sumnum']             #总用例
            total_successnum += i['successnum']     #成功用例
            total_failnum += i['failnum']           #失败用例
        total_skipnum = total_sumnum - (total_successnum + total_failnum)   #跳过用例


        #装饰测试报告封面
        self.exceltest.write_cover_info(cover,title,total_sumnum,total_successnum,total_failnum,total_skipnum,test_time)
        print('接口用例测试完毕，执行官结果如下:')
        print('本次接口用例共执行条数:%d'%total_sumnum)
        print('本次接口用例执行成功条数:%d'%total_successnum)
        print('本次接口用例执行失败条数:%d'%total_failnum)
        print('本次接口用例执行跳过条数:%d'%total_skipnum)
        print('请到{}路径下获取相关测试报告.'.format(execlreport_path))

if __name__=="__main__":
    excel=ExcelCreateReport()
    excel.create_report('abc')