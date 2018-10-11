CREATE TABLE T_DICTIONARY(
	DICTINARY          CHAR(20)     NOT NULL,
	CODE               CHAR(10)      NOT NULL,
	NAME               VARCHAR(500) NOT NULL,
	PRIMARY KEY(DICTINARY,CODE)
)

-- CREATE TABLE文を参照し、そのテーブルの文字コードを確認
-- show create table T_DICTIONARY;

-- テーブル状態を確認
-- SHOW TABLE STATUS FROM database;

-- 環境の文字コードを確認
-- SHOW VARIABLES LIKE "chara%";

-- 対象テーブルとカラムの文字コードを変更する
-- ALTER TABLE T_DICTIONARY CONVERT TO CHARACTER SET utf8;