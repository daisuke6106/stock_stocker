from argparse import ArgumentParser
from stock import stock_list

import mysql.connector
import matplotlib.pyplot as plt

def get_command_opritons():
    argparser = ArgumentParser()
    argparser.add_argument('-mh', '--mysql_host'    , type=str, help='mysql host'              )
    argparser.add_argument('-md', '--mysql_database', type=str, help='mysql database'          )
    argparser.add_argument('-mu', '--mysql_user'    , type=str, help='mysql user'              )
    argparser.add_argument('-mp', '--mysql_password', type=str, help='mysql password'          )
    argparser.add_argument('-s' , '--stock_no_list' , type=str, help='stock no list'           )
    return argparser.parse_args()

if __name__ == '__main__':
    options = get_command_opritons()
    # stock_no_list = options.stock_no_list.split(",")
    # stock_list_ = stock_list.new_instance_by_codelist(
    #     options.mysql_host, 
    #     options.mysql_database,
    #     options.mysql_user,
    #     options.mysql_password,
    #     stock_no_list
    # )
    
    stock_list_ = stock_list.new_instance_by_industry_code_17(
        options.mysql_host, 
        options.mysql_database,
        options.mysql_user,
        options.mysql_password,
        options.stock_no_list
    )
    stock_list_.plot_history("CLOSE_ADJUST_VALUE")
    plt.show()