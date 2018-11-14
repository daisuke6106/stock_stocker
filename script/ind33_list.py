from argparse import ArgumentParser
from stock import industry_code_33_list
import mysql.connector

def get_command_opritons():
    argparser = ArgumentParser()
    argparser.add_argument('-mh', '--mysql_host'    , type=str, help='mysql host'              )
    argparser.add_argument('-md', '--mysql_database', type=str, help='mysql database'          )
    argparser.add_argument('-mu', '--mysql_user'    , type=str, help='mysql user'              )
    argparser.add_argument('-mp', '--mysql_password', type=str, help='mysql password'          )
    return argparser.parse_args()

if __name__ == '__main__':
    options = get_command_opritons()
    connector = mysql.connector.connect(
        host     = options.mysql_host, 
        database = options.mysql_database, 
        user     = options.mysql_user, 
        password = options.mysql_password
    )
    ind33_list = industry_code_33_list(connector)
    for index, industry_code_33 in ind33_list.industry_code_33_list.iterrows() :
        print( industry_code_33.CODE + "," + industry_code_33.NAME )
        
    
    