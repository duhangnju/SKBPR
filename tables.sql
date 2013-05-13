BEGIN;

DROP TABLE IF EXISTS query_product;
DROP TABLE IF EXISTS query;
DROP TABLE IF EXISTS product;

CREATE TABLE IF NOT EXISTS query (
	id BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
	user_id VARCHAR(255) NOT NULL,
	query VARCHAR(255) NOT NULL,
	group_id SMALLINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS product (
	name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS query_product (
	id BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
	query_id BIGINT(10),
	product_name VARCHAR(255),
	bought INT(5), -- 0 stands for visit 1 stands for add to shopcart 2 stands for buy
    sequence INT
);

COMMIT;
