#!/user/bin/env python
#!encoding=utf-8
import unittest
from ddt import ddt,data
from Common.ExcelTools.ExcelddtTools import ExcelDDTTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.DataBaseTools import DataBaseTools

'''退出注销类api接口异常情况测试'''

@ddt
class API_TC_ABNL(unittest.TestCase):
    ddt_tools=ExcelDDTTools()
    data_list=ddt_tools.get_ddt_datalist('TC')

    @classmethod
    def setUpClass(self):
        self.exceltest = ExcelDDTTools()
        self.db = DataBaseTools()
        self.log = LogTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[TC_api_abnl_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.db.cur_close()  # 关闭游标
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[TC_api_abnl_end]<<<<<<<<<<<<<<<<<<<<<<')

    @data(*data_list)
    def test_tc_abnl(self,data):
        '''退出注销类-api接口异常用例'''
        self.exceltest.send_request(data)

if __name__=="__main__":
    unittest.main()