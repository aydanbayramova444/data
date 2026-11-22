-- name: overall
SELECT COUNT(*) AS tickets, ROUND(100.0 * AVG(met_sla), 1) AS sla_pct,
       ROUND(AVG(hours), 1) AS avg_hours, ROUND(AVG(csat), 2) AS csat
FROM tickets;

-- name: by_month
SELECT month, COUNT(*) AS tickets, ROUND(100.0 * AVG(met_sla), 1) AS sla_pct
FROM tickets GROUP BY month ORDER BY month;

-- name: by_category
SELECT category, COUNT(*) AS tickets, ROUND(100.0 * AVG(met_sla), 1) AS sla_pct,
       ROUND(100.0 * SUM(1 - met_sla) / SUM(SUM(1 - met_sla)) OVER (), 1) AS share_of_late_pct
FROM tickets GROUP BY category ORDER BY share_of_late_pct DESC;

-- name: by_channel
SELECT channel, COUNT(*) AS tickets, ROUND(100.0 * AVG(met_sla), 1) AS sla_pct
FROM tickets GROUP BY channel ORDER BY sla_pct;

-- name: by_shift
SELECT shift, COUNT(*) AS tickets, ROUND(100.0 * AVG(met_sla), 1) AS sla_pct
FROM tickets GROUP BY shift ORDER BY shift;

-- name: satisfaction
SELECT CASE met_sla WHEN 1 THEN 'On time' ELSE 'Late' END AS result,
       COUNT(csat) AS responses, ROUND(AVG(csat), 2) AS csat
FROM tickets GROUP BY met_sla ORDER BY met_sla DESC;
