#!/user/bin/env python
#!encoding=utf-8
import unittest
from ddt import ddt,data
from Common.ExcelTools.ExcelddtTools import ExcelDDTTools
from Common.CommonTools.LogTools import LogTools
from Common.CommonTools.DataBaseTools import DataBaseTools

'''数据采集类api接口异常情况测试'''

@ddt
class API_SJCJ_ABNL(unittest.TestCase):
    ddt_tools = ExcelDDTTools()
    data_list = ddt_tools.get_ddt_datalist('SJCJ')

    @classmethod
    def setUpClass(self):
        self.exceltest = ExcelDDTTools()
        self.db = DataBaseTools()
        self.log = LogTools()
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[SJCJ_api_abnl_start]<<<<<<<<<<<<<<<<<<<<')

    @classmethod
    def tearDownClass(self):
        self.db.cur_close()  # 关闭游标
        self.log.info('>>>>>>>>>>>>>>>>>>>>>[SJCJ_api_abnl_end]<<<<<<<<<<<<<<<<<<<<<<')

    @data(*data_list)
    def test_sjcj_abnl(self,data):
        '''数据采集类-api接口异常用例'''
        self.exceltest.send_request(data)

if __name__=="__main__":
    unittest.main()