--From the two most commonly appearing regions, which is the latest datasource?
SELECT data_source FROM trips
WHERE region in (SELECT region FROM trips GROUP BY region ORDER BY COUNT(1) DESC LIMIT 2)
ORDER BY datetime DESC LIMIT 1;

--What regions has the "cheap_mobile" datasource appeared in?
SELECT DISTINCT region FROM trips WHERE data_source = 'cheap_mobile';