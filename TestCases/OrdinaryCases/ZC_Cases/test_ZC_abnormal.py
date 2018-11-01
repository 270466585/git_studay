#!/user/bin/env python
#!encoding=utf-8
import unittest
from ddt import ddt,data
from Common.ExcelTools.ExcelddtTools import ExcelDDTTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.DataBaseTools import DataBaseTools

'''用户注册类api接口异常测试'''

@ddt
class API_ZC_ABNL(unittest.TestCase):
    '''用户注册类api接口异常测试'''
    #获取测试用例数据
    ddt_tools=ExcelDDTTools()
    data_list=ddt_tools.get_ddt_datalist('ZC')

    @classmethod
    def setUpClass(self):
        self.exceltest=ExcelDDTTools()
        self.db=DataBaseTools()
        self.log=LogTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[ZC_api_abnl_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.db.cur_close()  # 关闭游标
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[ZC_api_abnl_end]<<<<<<<<<<<<<<<<<<<<<<')

    @data(*data_list)        # 数据驱动
    def test_zc_abnl(self,data):
        '''用户注册类-api接口异常用例'''
        self.exceltest.send_request(data)

if __name__=="__main__":
    unittest.main()
