from argparse import ArgumentParser
from stock import stock

import mysql.connector
import matplotlib.pyplot as plt

def get_command_opritons():
    argparser = ArgumentParser()
    argparser.add_argument('-mh', '--mysql_host'    , type=str, help='mysql host'          )
    argparser.add_argument('-md', '--mysql_database', type=str, help='mysql database'      )
    argparser.add_argument('-mu', '--mysql_user'    , type=str, help='mysql user'          )
    argparser.add_argument('-mp', '--mysql_password', type=str, help='mysql password'      )
    argparser.add_argument('-s' , '--stock_no'      , type=str, help='Target stock nomber')
    return argparser.parse_args()

if __name__ == '__main__':
    options = get_command_opritons()
    connector = mysql.connector.connect(
        host     = options.mysql_host, 
        database = options.mysql_database, 
        user     = options.mysql_user, 
        password = options.mysql_password
        )
    stock_data = stock(connector, options.stock_no)
    stock_data.plot_stock_compariaon()
    plt.show()