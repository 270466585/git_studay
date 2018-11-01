#!/user/bin/env python
#!encoding=utf-8
import pymysql
from Common.CommonTools.PathTools import config_path
from Common.CommonTools.ConfigReadTools import ConfigReadTools

'''数据库操作相关函数'''

class DataBaseTools:
    def __init__(self):
        '''初始化-连接数据库'''
        self.conn=self._connent_db()    #连接数据库
        self.cur=self.conn.cursor()     #创建游标

    def _connent_db(self):
        '''连接数据库'''
        configread = ConfigReadTools(config_path)
        database_conf = configread.get_section_item('DATABASE_CONF')
        try:
            conn=pymysql.connect(host=database_conf['Host'],                #数据库地址
                                       port=int(database_conf['Port']),     #端口号
                                       user=database_conf['User'],          #登录用户名
                                       passwd=database_conf['Password'],    #登录密码
                                       db=database_conf['DB'],              #连接的数据库
                                       use_unicode=True, charset="utf8",)

            return conn
        except Exception as e:
            print('[Error] 数据库连接失败，具体错误:%s'%e)

    def execute_sql(self,sql):
        '''
        执行sql语句
        :param sql:sql语句
        '''
        try:
            self.cur.execute(sql)       #执行sql
        except Exception as e:
            self.conn.rollback()        #回退数据库
            print('[Error] sql语句有误，数据库回退，具体错误:%s'%e)
        else:
            self.conn.commit()          #sql正确时才进行提交

    def get_select_alldata(self,selectsql):
        '''
        获取查询sql对应的所有数据
        :param sql: select sql语句
        :return: 查询数据信息
        '''
        try:
            if 'Select' in selectsql or 'select' in selectsql or 'SELECT' in selectsql:
                self.cur.execute(selectsql)
        except Exception as e:
            self.conn.rollback()
            print('[Error] 查询sql语句有误.数据库回退，具体错误:%s'%e)
        else:
            try:
                result = self.cur.fetchall()  # 获取查询结果
                return result
            except Exception as a:
                print('[Error] 执行sql报错，具体错误:%s'%a)

    def get_selectdata_row(self,selectsql,index):
        '''
        获取查询sql反馈的某一行数据
        :param selectsql: 查询sql语句
        :param index: 指定一行数据
        :return: 反馈指定一行的数据
        '''
        result=self.get_select_alldata(selectsql)
        return result[index]

    def get_selectdata_column(self,selectsql,index):
        '''
        获取查询sql反馈的某一列数据
        :param selectsql:查询sql语句
        :param index:指定一列数据
        :return:反馈指定一列的数据
        '''
        column_data=[]
        result=self.get_select_alldata(selectsql)
        for i in range(len(result)):
            column_data.append(result[i][index])
        return column_data

    def get_specific_data(self,selectsql,rowindex,columnindex):
        '''
        获取指定的某一行的某一列的值，获取特定某个数据
        :param selectsql: 查询sql语句
        :param rowindex: 指定行数
        :param columnindex: 指定列数
        :return: 特定某个数据
        '''
        result=self.get_select_alldata(selectsql)
        return result[rowindex][columnindex]

    def check_value_isnull(self,selectsql,rowindex,columnindex):
        '''
        检查指定单元格的value是否为空，空返回True，非空返回False
        :param selectsql: 查询sql语句
        :param rowindex: 指定行数
        :param columnindex: 指定列数
        :return: True/False
        '''
        value=self.get_specific_data(selectsql,rowindex,columnindex)
        if value==None:
            return True
        else:
            return False

    def cur_close(self):
        '''关闭游标'''
        self.cur.close()

    def close_db(self):
        '''关闭数据库'''
        try:
            self.conn.close()
        except Exception as e:
            print('[Error] 数据库关闭出错.具体错误:%s'%e)



if __name__=="__main__":
    database=DataBaseTools()
    sql='select * from userinfo'
    # print(database.get_select_alldata(sql))
    # print(database.get_selectdata_column(sql,1))
    # print(database.get_specific_data(sql,0,2))
    print(database.get_selectdata_row(sql,0))
    # print(database.check_value_isnull(sql,0,4))
    print(database.get_specific_data(sql,0,0))
    database.cur_close()
    # print(database.select_data('select * from userinfo'))