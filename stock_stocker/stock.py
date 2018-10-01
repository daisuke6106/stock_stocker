'''
Created on 2018/09/15

@author: daisuke6106
'''

import os
import glob
import csv
import mysql.connector
import matplotlib

import pandas.io.sql as psql

import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance

class stock(object):
    '''
    classdocs
    '''
    
    # @staticmethod
    # def load_by_quandl(authtoken, stock_cd):
    #     quandl.ApiConfig.api_key = authtoken;
    #     return stock( quandl.get("XJPX/" + stock_cd) )

    @staticmethod
    def impoert_all_stock_csv_to_T_STOCK_QUOTE(basepath, mysql_host, mysql_database, mysql_user, mysql_password):
        base_dir       = os.listdir(basepath);
        stock_dir_list = [f for f in base_dir if os.path.isdir(os.path.join(basepath, f))]
        for stock_dir in stock_dir_list:
            stock.import_all_csv_to_T_STOCK_QUOTE(stock_dir, os.path.join(basepath, stock_dir) + "/*.csv", mysql_host, mysql_database, mysql_user, mysql_password)
            

    @staticmethod
    def import_all_csv_to_T_STOCK_QUOTE(stockcd, dirpath, mysql_host, mysql_database, mysql_user, mysql_password):
        files = glob.glob(dirpath)
        for filepath in files:
            stock.import_csv_to_T_STOCK_QUOTE(stockcd, filepath, mysql_host, mysql_database, mysql_user, mysql_password)
     
    @staticmethod
    def import_csv_to_T_STOCK_QUOTE(stockcd, filepath, mysql_host, mysql_database, mysql_user, mysql_password):
        connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
        cursor = connector.cursor()
        
        insert_sql = "REPLACE INTO T_STOCK_QUOTE VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        with open(filepath, "r", encoding='shift_jis') as file:
            reader = csv.reader(file)
            header1 = next(reader)
            header2 = next(reader)
            for row in reader:
                cursor.execute(insert_sql, [stockcd, row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
              
        connector.commit()
        connector.close()
         
    def __init__(self, stock_code, mysql_host, mysql_database, mysql_user, mysql_password):
        '''
        Constructor
        '''
        connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
        self.stock_info = psql.read_sql("SELECT * FROM T_STOCK WHERE CODE = %s", connector, params=[stock_code])
        # self.stock_history = psql.read_sql("SELECT * FROM T_STOCK_QUOTE WHERE CODE = %s", connector, params=[stock_code])
        self.stock_history = psql.read_sql("SELECT * FROM T_STOCK_QUOTE WHERE CODE = %s AND TRADDAY BETWEEN %s AND %s", connector, params=[stock_code, "2018-08-01", "2018-08-31" ])

    def plot_stock_history(self):
        fig = plt.figure(figsize=(18, 9))
        ax = fig.add_subplot(1,1,1)
        mpl_finance.candlestick2_ohlc(ax, 
                                      opens  = self.stock_history.OPEN_RATE, 
                                      highs  = self.stock_history.HIGH_PRICE, 
                                      lows   = self.stock_history.LOW_PRICE, 
                                      closes = self.stock_history.CLOSE_RATE, 
                                      width=1,
                                      colorup="b", 
                                      colordown="r")
        ax.set_xticklabels(
            [
                (self.stock_history.index[int(x)].strftime("%Y/%M/%D") if x < self.stock_history.shape[1] else x) for x in ax.get_xticks()
            ], rotation=90)
        ax.set_ylabel("Price")
        fig.show()
        # self.stock_history.plot()
        
    def save_to_db(self):
        pass


# class stock_metadata(object):
#     '''
#     classdocs
#     '''
#     
#     @staticmethod
#     def get_code_by_mysql(mysql_host, mysql_database, mysql_user, mysql_password):
#         connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
#         cursor = connector.cursor()
#         cursor.execute("SELECT CODE FROM T_QDL_XJPX_METADATA")
#         for row in cursor:
#             print(row[0])
#     
#     @staticmethod
#     def import_to_mysql(mysql_host, mysql_database, mysql_user, mysql_password, load_filepath):
#         
#         # create table T_QDL_XJPX_METADATA(
#         #   CODE VARCHAR(50),
#         #   NAME varchar(500),
#         #   DESCRIPTION varchar(1000),
#         #   REFRESHED_AT varchar(20),
#         #   FROM_DATE varchar(10),
#         #   TO_DATE varchar(10)
#         # );
#         connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
#         cursor = connector.cursor()
#         
#         insert_sql = "INSERT INTO T_QDL_XJPX_METADATA VALUES (%s, %s, %s, %s, %s, %s)"
#         with open(load_filepath, "r") as file:
#             reader = csv.reader(file)
#             header1 = next(reader)
#             header2 = next(reader)
#             for row in reader:
#                 cursor.execute(insert_sql, [row[0], row[1], row[2], row[3], row[4], row[5]])
#         connector.commit()
#         connector.close()
    
    
if __name__ == "__main__":
    '''
    メインメソッド
    '''
    # DBへのロード処理
    # stock_metadata.import_to_mysql( "192.168.42.124", "test_db", "test_user", "123456","/home/daisuke6106/ダウンロード/XJPX_metadata.csv")
    # stock.impoert_all_stock_csv_to_T_STOCK_QUOTE( "/media/daisuke6106/6fdc625a-0f9b-4cda-a50c-af5591ba0a5f/crawle_data/kabuoji3.com", "192.168.1.10", "test_db", "test_user", "123456")
    stock_data = stock("4847", "192.168.1.10", "test_db", "test_user", "123456")
    stock_data.plot_stock_history()
    print(stock_data)
    
