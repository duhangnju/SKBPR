-- select your database first and source this file.

SELECT COUNT(*) AS SESSION_NUMBER FROM user;

SELECT COUNT(*) AS SESSION_WITH_REFER_NUMBER FROM user U WHERE U.refer IS NOT NULL AND U.refer != '' AND U.refer != 'null';

SELECT COUNT(*) AS VISIT_NUMBER FROM visit;

SELECT COUNT(*) AS PRODUCT_VISIT_NUMBER FROM visit WHERE pagetype = 'product';

SELECT count(*) AS LAND_ON_HOMEPAGE_NUMBER FROM (SELECT U.userid, MIN(v.time), v.pagetype pt FROM user U JOIN visit V ON U.userid = V.userid WHERE U.refer IS NOT NULL AND U.refer != '' AND U.refer != 'null' GROUP BY V.userid) t WHERE pt = 'home';
