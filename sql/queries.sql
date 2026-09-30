-- SQLite 3: execute after loading data/clean/*.csv with scripts/validate_sql.py.
-- Counts are service-account keys, not verified people.
SELECT COUNT(*) AS service_accounts FROM customers_clean;

-- Exclusive risk groups use one maximum complete score per account.
WITH worst AS (
 SELECT customer_id, MAX(churn_risk_score) AS risk_score
 FROM customer_daily_metrics GROUP BY customer_id
)
SELECT CASE WHEN risk_score IS NULL THEN 'Insufficient history'
 WHEN risk_score >= 70 THEN 'High Risk' WHEN risk_score >= 40 THEN 'Medium Risk'
 ELSE 'Low Risk' END AS risk_category, COUNT(*) AS service_accounts
FROM worst GROUP BY risk_category;

-- Explicitly separate assigned and logged OLT; never silently equate them.
SELECT c.customer_id, c.olt_id AS assigned_olt, u.olt_id AS logged_olt,
 u.log_date, u.data_usage_gb, m.experience_score, m.churn_risk_score
FROM customers_clean c JOIN usage_logs_clean u USING(customer_id)
JOIN customer_daily_metrics m ON m.customer_id=u.customer_id AND m.log_date=u.log_date;

-- Complete, non-overlapping 7-calendar-day windows (integer Julian days).
WITH windows AS (
 SELECT customer_id, log_date,
 AVG(data_usage_gb) OVER (PARTITION BY customer_id ORDER BY julianday(log_date) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS current_mean,
 COUNT(data_usage_gb) OVER (PARTITION BY customer_id ORDER BY julianday(log_date) RANGE BETWEEN 6 PRECEDING AND CURRENT ROW) AS current_n,
 AVG(data_usage_gb) OVER (PARTITION BY customer_id ORDER BY julianday(log_date) RANGE BETWEEN 13 PRECEDING AND 7 PRECEDING) AS prior_mean,
 COUNT(data_usage_gb) OVER (PARTITION BY customer_id ORDER BY julianday(log_date) RANGE BETWEEN 13 PRECEDING AND 7 PRECEDING) AS prior_n
 FROM usage_logs_clean
)
SELECT customer_id,log_date,CASE WHEN current_n=7 AND prior_n=7 AND prior_mean>0
 THEN (prior_mean-current_mean)*100.0/prior_mean END AS usage_drop_percent FROM windows;

-- Decimal ratios; multiply by 100 only for textual percentage display.
SELECT olt_id,AVG(congestion_ratio) AS mean_daily_utilization,
 DENSE_RANK() OVER (ORDER BY AVG(congestion_ratio) DESC) AS utilization_rank
FROM olt_daily_metrics GROUP BY olt_id;

SELECT COUNT(DISTINCT customer_id) AS leakage_accounts
FROM customer_daily_metrics WHERE complaint_leakage_flag=1;

-- Source-system assignment conflicts by assigned OLT. This is a data-quality
-- queue, not evidence that an assigned OLT caused a customer's experience.
SELECT c.olt_id AS assigned_olt,
       COUNT(DISTINCT c.customer_id) AS service_accounts,
       COUNT(DISTINCT CASE WHEN c.olt_id <> u.olt_id THEN c.customer_id END) AS mismatched_accounts
FROM customers_clean c JOIN usage_logs_clean u USING(customer_id)
GROUP BY c.olt_id ORDER BY c.olt_id;

-- Coverage gap: absent logged OLTs are unknown, not healthy or zero utilization.
SELECT o.olt_id AS missing_logged_olt
FROM olt_info_clean o LEFT JOIN usage_logs_clean u ON o.olt_id=u.olt_id
WHERE u.olt_id IS NULL ORDER BY o.olt_id;
