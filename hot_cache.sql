BEGIN;

DROP TABLE IF EXISTS hot_cache;

CREATE TABLE hot_cache (
    product VARCHAR(255) PRIMARY KEY,
    weight FLOAT
);

INSERT INTO hot_cache
SELECT pageinfo, COUNT(id) count FROM visit
WHERE pagetype = 'product' AND pageinfo != ''
GROUP BY pageinfo ORDER BY count DESC LIMIT 20;

COMMIT;
