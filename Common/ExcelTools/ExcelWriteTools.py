#!/user/bin/env python
#!encoding=utf-8
import time
import xlsxwriter
from Common.CommonTools.ConfigReadTools import ConfigReadTools
from Common.CommonTools.PathTools import config_path,execlreport_path
'''编辑Excel文件函数封装'''

class ExcelWriteTools:
    def __init__(self,reportname=None):
        '''数据配置'''
        #读取配置文件获取数据
        readconfig=ConfigReadTools(config_path)
        tabledict=readconfig.get_section_item('TABLE_DATA')
        self.project_name=tabledict['Project_name']         #项目名称
        self.version=tabledict['Version']                   #版本号
        self.script=tabledict['Scripting_language']         #脚本语言
        self.internet=tabledict['Internet']                 #网络
        #其他配置数据
        self.createtime=time.strftime('%Y%m%d-%H:%M:%S')    #创建时间
        self.reportname=self._set_reportname(reportname)    #创建名称
        self.reportfilepath=execlreport_path+self.reportname #文件完整路径
        #编辑文件
        self.workbook=xlsxwriter.Workbook(self.reportfilepath)  #创建xlsx文件

    def _set_reportname(self,name=None):
        '''
        设置报告名称
        :param name: 名称
        '''
        if name!=None:
            nowtime = time.strftime('%Y-%m-%d-%H-%M-%S')  # 当前时间
            reportname='%s_%s.xlsx'%(name,nowtime)
            return reportname
        else:
            nowtime = time.strftime('%Y-%m-%d-%H-%M-%S')  # 当前时间
            reportname = 'ExcelReport_%s.xlsx' % nowtime  # 文件名称
            return reportname


    def add_worksheet(self,sheetname):
        '''
        添加工作sheet
        :param sheetname:sheet名称
        '''
        return self.workbook.add_worksheet(sheetname)

    def add_chartsheet(self,sheetname):
        '''
        添加图标sheet
        :param sheetname:sheet名称
        '''
        return self.workbook.add_chartsheet(sheetname)

    def create_cover_gui(self,worksheet,title,sumnum,successnum,failnum,skipnum,usetime):
        '''
        创建ExcelReport测试报告封面
        :param worksheet: 工作sheet
        :param title: 测试报告主题
        :param sumnum: 总用例个数
        :param successnum: 成功用例个数
        :param failnum: 失败用例个数
        :param skipnum: 跳过用例个数
        :param usetime: 执行时间
        '''

        #设置列宽
        self.set_column(worksheet,'A:A',15)
        self.set_column(worksheet,'B:B',20)
        self.set_column(worksheet,'C:C',30)
        self.set_column(worksheet,'D:D',20)
        self.set_column(worksheet,'E:E',15)
        self.set_column(worksheet,'F:F',15)

        #编辑title
        title_format=self.set_coverformat(bg_color='#FFFF00')   #单元格样式
        self.set_row(worksheet,0,40)                           #title单元格高度
        self.write_merge_range(worksheet,'A1:F1',title,title_format)  #编辑title

        #编辑概况
        gaikuang_format=self.set_coverformat(font_size=13,bg_color='#99CC00')
        self.set_row(worksheet,1,25)
        self.write_merge_range(worksheet,'A2:F2','测试概况',gaikuang_format)

        #编辑BODY
        body_format=self.set_coverformat(font_size=13)
        self.set_allrows(worksheet,2,6,25)
        self.write_merge_range(worksheet,'A3:A7','接口自动化',body_format)
        #设定body内容
        body={
            'project_name':self.project_name,
            'version':self.version,
            'script':self.script,
            'createtime':self.createtime,
            'sumnum':sumnum,
            'successnum':successnum,
            'failnum':failnum,
            'skipnum':skipnum,
            'usetime':usetime,
            'tester':'罗泽霖'
        }
        #计算用例执行成功率
        success_point=float(successnum/sumnum*100)
        #指定单元格插入body内容
        self.write_cell(worksheet,'B3','项目名称',body_format)
        self.write_cell(worksheet,'C3',body['project_name'],body_format)
        self.write_cell(worksheet,'D3','接口总数',body_format)
        self.write_cell(worksheet,'E3',body['sumnum'],body_format)
        self.write_cell(worksheet,'B4','接口版本',body_format)
        self.write_cell(worksheet,'C4',body['version'],body_format)
        self.write_cell(worksheet,'D4','成功个数',body_format)
        self.write_cell(worksheet,'E4',body['successnum'],body_format)
        self.write_cell(worksheet,'B5','脚本语言',body_format)
        self.write_cell(worksheet,'C5',body['script'],body_format)
        self.write_cell(worksheet,'D5','失败个数',body_format)
        self.write_cell(worksheet,'E5',body['failnum'],body_format)
        self.write_cell(worksheet,'B6','创建时间',body_format)
        self.write_cell(worksheet,'C6',body['createtime'],body_format)
        self.write_cell(worksheet,'D6','跳过个数',body_format)
        self.write_cell(worksheet,'E6',body['skipnum'],body_format)
        self.write_cell(worksheet,'B7','测试人员',body_format)
        self.write_cell(worksheet,'C7',body['tester'],body_format)
        self.write_cell(worksheet,'D7','通过百分比',body_format)
        self.write_cell(worksheet,'E7','%.2f'%success_point+'%',body_format)
        self.write_cell(worksheet,'F3','执行时间',body_format)
        self.write_merge_range(worksheet,'F4:F7','%ss'%body['usetime'],body_format)
        #创建饼图
        self.create_pie(worksheet)

    def create_table_gui(self,worksheet):
        '''
        创建测试详情表的样式
        :param sheetname: 工作表名称
        '''
        #设置格式
        body_format=self.set_cellformat(bg_color='#CCFFFF')
        #设置列宽
        self.set_column(worksheet,'A:A',10)    #用例id
        self.set_column(worksheet,'B:B',20)    #模块名称
        self.set_column(worksheet,'C:C',20)    #用例内容
        self.set_column(worksheet,'D:D',20)    #url
        self.set_column(worksheet,'E:E',20)    #请求方式
        self.set_column(worksheet,'F:F',20)    #header参数
        self.set_column(worksheet,'G:G',20)    #url参数
        self.set_column(worksheet,'H:H',20)    #data参数
        self.set_column(worksheet,'I:I',20)    #响应信息
        self.set_column(worksheet,'J:J',20)    #预期errorCode
        self.set_column(worksheet,'K:K',20)    #实际errorCode
        self.set_column(worksheet,'L:L',20)    #预期isTrue
        self.set_column(worksheet,'M:M',20)    #实际isTrue
        self.set_column(worksheet,'N:N',20)    #预期errorMessage
        self.set_column(worksheet,'O:O',20)    #实际errorMessage
        self.set_column(worksheet,'P:P',20)    #测试结果

        #设置内容
        self.write_cell(worksheet,'A1','用例ID',body_format)
        self.write_cell(worksheet,'B1','模块名称',body_format)
        self.write_cell(worksheet,'C1','用例内容',body_format)
        self.write_cell(worksheet,'D1','URL',body_format)
        self.write_cell(worksheet,'E1','请求方式',body_format)
        self.write_cell(worksheet,'F1','header参数',body_format)
        self.write_cell(worksheet,'G1','url参数',body_format)
        self.write_cell(worksheet,'H1','data参数',body_format)
        self.write_cell(worksheet,'I1','响应信息',body_format)
        self.write_cell(worksheet,'J1','预期errorCode',body_format)
        self.write_cell(worksheet,'K1','实际errorCode',body_format)
        self.write_cell(worksheet,'L1','预期isTrue',body_format)
        self.write_cell(worksheet,'M1','实际isTrue',body_format)
        self.write_cell(worksheet,'N1','预期errorMessage',body_format)
        self.write_cell(worksheet,'O1','实际errorMessage',body_format)
        self.write_cell(worksheet,'P1','测试结果',body_format)

    def create_pie(self,worksheet):
        '''
        创建饼图
        :param title: 标题
        '''
        #生成饼状图
        piechart=self.workbook.add_chart({'type': 'pie'})
        #获取饼图内容以及饼图值，设置饼图颜色（通过用例-绿色、失败用例-红色、跳过用例-灰色）
        piechart.add_series({'name':'车之联接口测试执行情况','categories': '=报告概况!$D$4:$D$6','values': '=报告概况!$E$4:$E$6',
                             "points": [{"fill": {"color": "#339966"}},{"fill": {"color": "#993366"}},{"fill": {"color": "#CCCCFF"}}]})
        piechart.set_title({'name':'车之联接口测试执行情况'})
        piechart.set_style(2)   #设置样式
        #插入饼图，设置插入位置以及图形大小
        worksheet.insert_chart('A9', piechart, {'x_offset': 180, 'y_offset': 10})

    def get_all_workbooks(self):
        '''获取所有工作簿'''
        return self.workbook.worksheets()

    def get_worksheet_byname(self,sheetname):
        '''
        通过sheetname获取工作表
        :param sheetname: sheet名称
        '''
        return self.workbook.get_worksheet_by_name(sheetname)

    def write_cell(self,worksheet,cell,data,format):
        '''
        编辑单元格内容
        :param worksheet:工作sheet
        :param cell: 单元格
        :param data: 编辑内容
        :param format: 单元格样式
        '''
        return worksheet.write(cell,data,format)

    def write_pass(self,worksheet,cell):
        '''
        编辑单元格内容为PASS
        :param worksheet: 工作sheet
        :param cell: 单元格
        :param format: 单元格样式
        '''
        format=self.set_cellformat(bg_color='#99CC00')
        worksheet.write(cell,'PASS',format)

    def write_fail(self,worksheet,cell):
        '''
        编辑单元格内容为FAIL
        :param worksheet: 工作sheet
        :param cell: 单元格
        :param format: 单元格样式
        '''
        format=self.set_cellformat(bg_color='#FF0000')
        worksheet.write(cell,'FAIL',format)

    def write_na(self,worksheet,cell):
        '''
        编辑单元格内容为N/A
        :param worksheet: 工作sheet
        :param cell: 单元格
        :return: 单元格样式
        '''
        format=self.set_cellformat(bg_color='#C0C0C0')
        worksheet.write(cell,'N/A',format)

    def write_merge_range(self,worksheet,rangecell,data,format):
        '''
        合并单元格并写入数据
        :param worksheet: 工作表
        :param rangecell: 合并单元格范围，例如'D1:D7'
        :param data: 写入数据信息
        :param format: 单元格样式
        '''
        worksheet.merge_range(rangecell,data,format)


    def set_sheetcolor(self,worksheet,color):
        '''
        设置标签颜色
        :param worksheet: 工作表
        '''
        worksheet.set_tab_color(color)

    def set_row(self,worksheet,rownum,height):
        '''
        设置整行高度
        :param worksheet: 工作表
        :param rownum: 第几行，index
        :param size: 高度
        '''
        worksheet.set_row(rownum,height)

    def set_allrows(self,worksheet,startrow,endrow,height):
        '''
        设置规定范围的行的高度
        :param worksheet: 工作表
        :param startrow: 开始行
        :param endrow: 结束行
        :param height: 高度
        '''
        for i in range(startrow,endrow+1):
            self.set_row(worksheet,i,height)

    def set_column(self,worksheet,rangecell,width):
        '''
        设置列宽度
        :param worksheet: 工作表
        :param rangecell: 列范围，例如'A1:A5',也可以是相同的'A:A'
        :param width: 宽度
        '''
        worksheet.set_column(rangecell,width)

    def set_coverformat(self,font_size=14,bg_color='#FFFFFF',font_color='#000000',bordernum=1,font_name='微软雅黑'):
        '''
        设置单元格样式
        :param font_size:字体大小(默认14号)
        :param bg_color: 背景颜色（默认白色）
        :param font_color: 字体颜色（默认黑色）
        :param bordernum: 边框值(默认1-有)
        :param font_name: 字体(默认微软雅黑)
        :return: 单元格样式
        '''
        cover_style=self.workbook.add_format(
            {'align':'center','valign':'vcenter','border': bordernum, 'font_size': font_size, 'bg_color': bg_color,
             'font_color': font_color,'font_name':font_name})
        return cover_style

    def set_cellformat(self,font_size=12,bg_color='#FFFFFF',font_color='#000000',bordernum=1,font_name='微软雅黑',text_wrap=1):
        '''
        设置单元格样式
        :param font_size:字体大小(默认12号)
        :param bg_color: 背景颜色（默认白色）
        :param font_color: 字体颜色（默认黑色）
        :param bordernum: 边框值(默认1-有)
        :param font_name: 字体(默认微软雅黑)
        :param text_wrap: 自动换行（默认1-自动换行）
        :return: 单元格样式
        '''
        cell_style = self.workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'border': bordernum, 'font_size': font_size, 'bg_color': bg_color,
             'font_color': font_color, 'font_name': font_name,'text_wrap':text_wrap})
        return cell_style

    def set_workbook_size(self, width, height):
        '''
        设置工作簿窗口大小
        :param width: 宽度
        :param height: 高度
        '''
        return self.workbook.set_size(width, height)


    def close_workbook(self):
        '''关闭xlsx文件'''
        self.workbook.close()

if __name__=="__main__":
    excel=ExcelWriteTools('test')
    excel.create_cover_gui('车之联API接口测试报告')
    sheet1 = excel.add_worksheet('活动')
    sheet2=excel.add_worksheet('加油')
    excel.create_table_gui(sheet1)
    excel.create_table_gui(sheet2)
    # abc=excel.add_worksheet('abc')
    # headings=['name','sex','age']
    # data=[
    #     ['luozelin','female',29],
    #     ['zengwenjing','male',29]
    # ]
    # format1=excel.set_coverformat()
    # format2=excel.set_coverformat(bg_color='#99CC00')
    # #设置宽度
    # excel.set_allrows(abc,4,50)
    # #设置高度
    # excel.set_column(abc,'A:C',30)
    # #写入数据
    # excel.write_merge_range(abc,'A1:C1','接口测试报告',format2)
    # excel.write_row(abc,'A2',headings,format1)
    # excel.write_row(abc,'A3',data[0],format1)
    # excel.write_row(abc,'A4',data[1],format1)


    excel.close_workbook()