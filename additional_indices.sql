-- additional INDICES on original tables to speed up processing
ALTER TABLE user ADD INDEX (userid);
ALTER TABLE user ADD INDEX (refer);

ALTER TABLE visit ADD INDEX (userid);
ALTER TABLE visit ADD INDEX (pagetype);
ALTER TABLE visit ADD INDEX (pageinfo);
ALTER TABLE visit ADD INDEX (time);

ALTER TABLE orderrecord ADD INDEX (userid);
ALTER TABLE orderrecord ADD INDEX (item);
