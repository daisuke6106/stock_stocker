#!/bin/bash
# ====================================================================================================
# 環境設定
# ====================================================================================================
export PYTHONPATH="../stock_stocker:$PYTHONPATH"

# ====================================================================================================
# MYSQL接続先設定
# ====================================================================================================
export MYSQL_HOST="192.168.42.124"
export MYSQL_DATABASE="test_db"
export MYSQL_USER="test_user"
export MYSQL_PASSWORD="123456"