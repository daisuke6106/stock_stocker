'''
Created on 2018/09/15

@author: daisuke6106
'''

import os
import glob
import csv
import mysql.connector

import pandas.io.sql as psql

import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance

class industry_code_17(object):
    '''
    classdocs
    '''
    @staticmethod
    def new_instance(mysql_host, mysql_database, mysql_user, mysql_password, code):
        connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
        return industry_code_17(connector, code)

    def __init__(self, connector, code):
        self.connector = connector
        self.code = code
        self.industry_code = psql.read_sql("SELECT * FROM V_INDUSTRY_CODE_17 WHERE CODE = %s", self.connector, params=[code])
        stock_code_list = psql.read_sql("SELECT * FROM T_STOCK WHERE INDUSTRY_CODE_17 = %s", self.connector, params=[code])
        
        self.stock_list = []
        for stock_code in self.stock_code_list :
            self.stock_list.append(stock(self.connector, stock_code.CODE))


class stock_list(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def new_instance_by_industry_code_17(mysql_host, mysql_database, mysql_user, mysql_password, industry_code_17, start = "1980-01-01", stop = "9999-12-31"):
        connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
        stock_code_list = []
        for index, stock in psql.read_sql("SELECT * FROM T_STOCK WHERE INDUSTRY_CODE_17 = %s", connector, params=[industry_code_17]).iterrows() :
            stock_code_list.append(stock["CODE"])
        return stock_list(connector, stock_code_list, start, stop)
    
    @staticmethod
    def new_instance_by_codelist(mysql_host, mysql_database, mysql_user, mysql_password, stock_code_list, start = "1980-01-01", stop = "9999-12-31"):
        connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
        return stock_list(connector, stock_code_list, start, stop)

    def __init__(self, connector, stock_code_list, start = "1980-01-01", stop = "9999-12-31"):
        self.connector = connector
        self.stock_list = []
        for stock_code in stock_code_list :
            self.stock_list.append(stock(connector, stock_code, start, stop))

    def plot_history(self, plot_target):
        tmp_df_list = []
        for stock in self.stock_list :
            tmp_df = stock.stock_history[plot_target]
            tmp_df.rename(columns={plot_target : stock.stock_code})
            tmp_df_list.append(tmp_df)
        tmp_marged_df = pd.concat(tmp_df_list, axis=1)
        tmp_marged_df.plot()

class stock(object):
    '''
    classdocs
    '''
    
    # @staticmethod
    # def load_by_quandl(authtoken, stock_cd):
    #     quandl.ApiConfig.api_key = authtoken;
    #     return stock( quandl.get("XJPX/" + stock_cd) )

    @staticmethod
    def new_instance(mysql_host, mysql_database, mysql_user, mysql_password, stock_code, start = "1980-01-01", stop = "9999-12-31"):
        '''
        Constructor
             引数に指定された接続先のDBに存在する以下のテーブルより指定された銘柄の情報を指定の期間取得し、株価オブジェクトを生成する。
             銘柄情報を保持する「T_STOCK」、
             株価過去情報を保持する「T_STOCK_QUOTE」より
        Parameters
        ----------
        mysql_host : str
            MYSQL接続先ホスト、もしくはIPアドレス
        mysql_database : str
            MYSQL接続先データベース名
        mysql_user : str
            MYSQL接続先ユーザ名
        mysql_password : str
            MYSQL接続先パスワード
        stock_code : str
            株価コード
        start : str, default 1980-01-01
            取得期間(From) 
        stop : str, default 9999-12-31
            取得期間(To)
        '''
        connector = mysql.connector.connect(host = mysql_host, database = mysql_database, user=mysql_user, password = mysql_password)
        return stock(connector, stock_code, start, stop)

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
         
    
         
    def __init__(self, connector, stock_code, start = "1980-01-01", stop = "9999-12-31"):
        '''
        Constructor
             引数に指定された接続先のDBに存在する以下のテーブルより指定された銘柄の情報を指定の期間取得し、株価オブジェクトを生成する。
             銘柄情報を保持する「T_STOCK」、
             株価過去情報を保持する「T_STOCK_QUOTE」より取得しインスタンスを生成する。
        Parameters
        ----------
        connector : mysql.connector
            MYSQLへの接続確立済みコネクション
        stock_code : str
            株価コード
        start : str, default 1980-01-01
            取得期間(From) 
        stop : str, default 9999-12-31
            取得期間(To)
        '''
        self.connector = connector
        self.stock_code = stock_code
        self.stock_info = psql.read_sql("SELECT * FROM T_STOCK WHERE CODE = %s", self.connector, params=[stock_code])
        self.stock_history = psql.read_sql("SELECT * FROM V_STOCK_HISTORY WHERE CODE = %s AND TRADDAY BETWEEN %s AND %s ORDER BY TRADDAY", self.connector, params=[stock_code, start, stop], index_col="TRADDAY")
        

    def save_day_before_ratio(self):
        '''
        現在、インスタンスが保持している期間の「調整後終値」をもとに前日比を算出し、「T_STOCK_COMPARIAON」へ格納する。
        '''
        cursor = self.connector.cursor()
        insert_sql = "REPLACE INTO T_STOCK_COMPARIAON VALUES (%s, %s, %s, %s)"
        
        day_before_ratio_list = self.create_day_before_ratio()
        for trad_day, day_before_ratio in day_before_ratio_list.iterrows() : 
            cursor.execute(insert_sql, [self.stock_code, trad_day, day_before_ratio.DAY_BEFORE_RATIO, day_before_ratio.DAY_BEFORE_RATIO_HISTORY])
        self.connector.commit()
        
    def create_day_before_ratio(self):
        stock_rate_of_change = pd.DataFrame(columns=["DAY_BEFORE_RATIO","DAY_BEFORE_RATIO_HISTORY"])
        before_row_history = None
        day_before_ratio_history = 0
        for trad_day, row_history in self.stock_history.iterrows() :
            if before_row_history is not None:
                day_before_ratio = ( ( row_history.CLOSE_ADJUST_VALUE - before_row_history.CLOSE_ADJUST_VALUE ) / before_row_history.CLOSE_ADJUST_VALUE ) * 100
                day_before_ratio_history = day_before_ratio_history + day_before_ratio
                stock_rate_of_change.loc[trad_day] = [day_before_ratio, day_before_ratio_history]
            before_row_history = row_history
        return stock_rate_of_change

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
     
    def plot_stock_compariaon(self):
        self.stock_history[['CLOSE_ADJUST_VALUE', 'DAY_BEFORE_RATIO_HISTORY']].plot()
        
     
    def save_to_db(self):
        pass

if __name__ == "__main__":
    '''
    メインメソッド
    '''
    stock_list_ = stock_list.new_instance_by_industry_code_17(
        "192.168.1.13", 
       "test_db",
       "test_user",
        "123456",
        "1"
    )
    stock_list_.plot_history("CLOSE_ADJUST_VALUE")
    plt.show()
    
    
    
