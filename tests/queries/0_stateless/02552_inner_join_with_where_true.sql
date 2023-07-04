CREATE TABLE t0 (c0 Int32) ENGINE = Memory;
CREATE TABLE t1 (c1 Int32) ENGINE = Memory;

INSERT INTO t0(c0) VALUES (1), (2);
INSERT INTO t1(c1) VALUES (1);

SELECT max(1), count() FROM t0 AS t0 LEFT JOIN t1 ON true WHERE 1;
SELECT max(1), count() FROM t0 AS t0 INNER JOIN t1 ON t0.c0 = t1.c1 WHERE 1;
SELECT max(1), count() FROM t0 AS t0 INNER JOIN t1 ON true WHERE 0;
