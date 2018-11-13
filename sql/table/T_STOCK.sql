CREATE TABLE T_STOCK(
	APPLYDATE          CHAR(8)      NOT NULL,
	CODE               CHAR(4)      NOT NULL,
	NAME               VARCHAR(500) NOT NULL,
	MERKET_PROD_DIV    CHAR(3),
	INDUSTRY_CODE_33   CHAR(4),
	INDUSTRY_CODE_17   CHAR(2),
	SCALE_CODE         CHAR(1),
	PRIMARY KEY(APPLYDATE,CODE)
)

-- CREATE TABLE文を参照し、そのテーブルの文字コードを確認
-- show create table T_STOCK;

-- テーブル状態を確認
-- SHOW TABLE STATUS FROM database;

-- 環境の文字コードを確認
-- SHOW VARIABLES LIKE "chara%";

-- 対象テーブルとカラムの文字コードを変更する
-- ALTER TABLE T_STOCK CONVERT TO CHARACTER SET utf8;