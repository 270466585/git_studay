#!/user/bin/env python
#!encoding=utf-8
import unittest
from ddt import ddt,data
from Common.ExcelTools.ExcelddtTools import ExcelDDTTools
from Common.CommonTools.LogTools import LogTools

'''好友类api接口异常情况测试'''

@ddt
class API_HY_ABNL(unittest.TestCase):
    ddt_tools = ExcelDDTTools()
    data_list = ddt_tools.get_ddt_datalist('HY')

    @classmethod
    def setUpClass(self):
        self.exceltest = ExcelDDTTools()
        self.log = LogTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[HY_api_abnl_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[HY_api_abnl_end]<<<<<<<<<<<<<<<<<<<<<<')

    @data(*data_list)
    def test_hy_abnl(self,data):
        '''好友类-api接口异常用例'''
        self.exceltest.send_request(data)

if __name__=="__main__":
    unittest.main()