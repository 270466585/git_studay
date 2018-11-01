#!/user/bin/env python
#!encoding=utf-8
import unittest
from ddt import ddt,data
from Common.ExcelTools.ExcelddtTools import ExcelDDTTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.DataBaseTools import DataBaseTools

'''用户登录类api接口异常情况测试'''

@ddt
class API_DL_ABNL(unittest.TestCase):
    ddt_tools=ExcelDDTTools()
    data_list=ddt_tools.get_ddt_datalist('DL')

    @classmethod
    def setUpClass(self):
        self.exceltest = ExcelDDTTools()
        self.db = DataBaseTools()
        self.log = LogTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[DL_api_abnl_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.db.cur_close()  # 关闭游标
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[DL_api_abnl_end]<<<<<<<<<<<<<<<<<<<<<<')

    @data(*data_list)
    def test_dl_abnl(self,data):
        '''用户登录类-api接口异常情况测试'''
        self.exceltest.send_request(data)

if __name__=="__main__":
    unittest.main()