#!/user/bin/env python
#!encoding=utf-8
import xlrd

'''Excel文件读取相关封装函数'''
'''
[Sheet] DL-登录 / HDGGYY-活动广告运营 / HY-好友 / PDDT-频道电台 / SJCJ-数据采集 /
        TC-退出 / USER-用户 / WJGJ-文件处理、工具 / XTPZ-系统配置 / ZC-注册 /
'''

class ExcelReadTools:
    def __init__(self,excelpath):
        '''打开指定的excel文件'''
        self.excelread=xlrd.open_workbook(excelpath)

    def get_AllSheets(self):
        '''获取所有的sheets'''
        sheets=self.excelread.sheet_names()
        return sheets

    def get_SheetbyName(self,sheetname):
        '''
        通过name获取指定的sheet
        :param sheetname: sheet名称
        :return: sheet
        '''
        sheet=self.excelread.sheet_by_name(sheetname)
        return sheet

    def get_nrows(self,sheetname):
        '''
        获取指定sheet的行数
        :param sheetname:sheet名称
        :return: sheet总行数
        '''
        sheet=self.get_SheetbyName(sheetname)
        rows_num=sheet.nrows
        return rows_num

    def get_ncolumns(self,sheetname):
        '''
        获取指定sheet的列数
        :param sheetname:sheet名称
        :return: sheet总列数
        '''
        sheet=self.get_SheetbyName(sheetname)
        columns_num=sheet.ncols
        return columns_num

    def get_value(self,sheetname,row,col):
        '''
        通过行、列定位单元格获取value
        :param row: 行
        :param col: 列
        :return: 单元格value
        '''
        sheet=self.get_SheetbyName(sheetname)
        getvalue=sheet.cell_value(row,col)
        return getvalue

    def get_row_values(self,sheetname,row):
        '''
        获取excel一行的数据
        :param sheetname:sheet名称
        :param row: 行数
        :return: 返回一行的数据
        '''
        row_value_list=[]
        sheet=self.get_SheetbyName(sheetname)
        sheet_row_len=sheet.ncols       #通过列数获取一行元素的长度
        for i in range(sheet_row_len):
            get_value=self.get_value(sheetname,row,i)
            row_value_list.append(get_value)
        return row_value_list

    def get_column_values(self,sheetname,col):
        '''
        获取excel一列的数据
        :param sheetname:sheet名称
        :param col: 列数
        :return: 返回一列的数据
        '''
        col_value_list=[]
        sheet=self.get_SheetbyName(sheetname)
        sheet_column_len=sheet.nrows    #通过行数获取一列元素的长度
        for i in range(sheet_column_len):
            get_value=self.get_value(sheetname,i,col)
            col_value_list.append(get_value)
        return col_value_list


    

if __name__=="__main__":
    excelread=ExcelReadTools(r'D:\linkofcar_api\Data\Data_API.xlsx')
   # print(excelread.get_AllSheets())
    #print(excelread.get_SheetbyName('DL'))
    #print(excelread.get_nrows('DL'))
    #print(excelread.get_ncolumns('DL'))
    #print(excelread.get_value('DL',0,1))
    print(excelread.get_row_values('DL',1))
    #print(excelread.get_column_values('DL',2))