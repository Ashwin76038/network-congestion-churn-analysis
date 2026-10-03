-- MySQL 8: run against the loaded public model tables.
-- accounts
SELECT COUNT(*) FROM customers_clean;
-- account_days
SELECT COUNT(*) FROM usage_logs_clean;
-- scenario_days
SELECT COUNT(DISTINCT log_date) FROM usage_logs_clean;
-- logged_olts
SELECT COUNT(DISTINCT olt_id) FROM usage_logs_clean;
-- assigned_groups
SELECT COUNT(*) FROM olt_info_clean;
-- mismatch_accounts
SELECT COUNT(DISTINCT u.customer_id) FROM usage_logs_clean u JOIN customers_clean c USING(customer_id) WHERE u.olt_id<>c.olt_id;
-- scored_rows
SELECT COUNT(churn_risk_score) FROM customer_daily_metrics;
-- complete_windows
SELECT COUNT(*) FROM (SELECT customer_id,log_date,COUNT(*) OVER (PARTITION BY customer_id ORDER BY TO_DAYS(log_date) RANGE BETWEEN 13 PRECEDING AND CURRENT ROW) AS n14,SUM(data_usage_gb) OVER (PARTITION BY customer_id ORDER BY TO_DAYS(log_date) RANGE BETWEEN 13 PRECEDING AND 7 PRECEDING) AS prior_usage FROM usage_logs_clean) w WHERE n14=14 AND prior_usage>0;
-- mean_ratio
SELECT AVG(congestion_ratio) FROM olt_daily_metrics;
-- ratio_max_error
SELECT MAX(ABS(n.congestion_ratio-(u.gb*8/86400/o.capacity_gbps))) FROM olt_daily_metrics n JOIN (SELECT olt_id,log_date,SUM(data_usage_gb) gb FROM usage_logs_clean GROUP BY olt_id,log_date) u USING(olt_id,log_date) JOIN logged_olt o USING(olt_id);
-- complaints
SELECT COUNT(*) FROM complaints;
-- withheld_dates
SELECT SUM(activation_date_withheld_flag) FROM customers_clean;
