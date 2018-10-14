#!/bin/bash
# ====================================================================================================
# 環境設定部
# ====================================================================================================
source ../bin/activate
source ./env.sh

python << EOF
import os
import glob
import csv
import mysql.connector
import matplotlib
import pandas.io.sql as psql
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance

import stock 

connector = mysql.connector.connect(host = "${MYSQL_HOST}", database = "${MYSQL_DATABASE}", user="${MYSQL_USER}", password = "${MYSQL_PASSWORD}")
stock_data = stock(connector, "4847")
stock_data.stock_data.plot_stock_compariaon()
EOF