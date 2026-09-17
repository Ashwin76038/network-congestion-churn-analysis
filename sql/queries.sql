-- Network Experience, OLT Congestion & Customer Risk Analytics
-- SQL examples assume a database schema with the clean CSV files loaded as tables.

-- 1. Business question: What does the combined customer, plan, usage, and OLT analysis view look like?
SELECT
    c.customer_id,
    c.area,
    p.plan_tier,
    p.value_segment,
    u.log_date,
    u.data_usage_gb,
    u.avg_speed_mbps,
    u.downtime_minutes,
    u.latency_ms,
    m.experience_score,
    m.churn_risk_score,
    m.churn_risk_category,
    o.olt_id,
    o.capacity_gbps
FROM customers_clean c
JOIN plans_clean p ON c.plan_id = p.plan_id
JOIN usage_logs_clean u ON c.customer_id = u.customer_id
JOIN customer_daily_metrics m
  ON u.customer_id = m.customer_id
 AND u.log_date = m.log_date
JOIN olt_info_clean o ON c.olt_id = o.olt_id;

-- 2. Business question: How many customers are in each churn risk category before slicers?
SELECT churn_risk_category, COUNT(DISTINCT customer_id) AS customers
FROM customer_daily_metrics
GROUP BY churn_risk_category
ORDER BY customers DESC;

-- 3. Business question: What are rolling 7-day customer usage averages?
WITH rolling_usage AS (
    SELECT
        customer_id,
        log_date,
        data_usage_gb,
        AVG(data_usage_gb) OVER (
            PARTITION BY customer_id
            ORDER BY log_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS current_7d_avg
    FROM usage_logs_clean
)
SELECT *
FROM rolling_usage
ORDER BY customer_id, log_date;

-- 4. Business question: Which customers show the biggest drop versus the previous rolling average?
WITH rolling_usage AS (
    SELECT
        customer_id,
        log_date,
        data_usage_gb,
        AVG(data_usage_gb) OVER (
            PARTITION BY customer_id
            ORDER BY log_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS current_7d_avg
    FROM usage_logs_clean
),
drop_calc AS (
    SELECT
        *,
        LAG(current_7d_avg) OVER (PARTITION BY customer_id ORDER BY log_date) AS previous_7d_avg
    FROM rolling_usage
)
SELECT
    customer_id,
    log_date,
    current_7d_avg,
    previous_7d_avg,
    CASE
        WHEN previous_7d_avg IS NULL OR previous_7d_avg = 0 THEN NULL
        ELSE ((previous_7d_avg - current_7d_avg) / previous_7d_avg) * 100
    END AS usage_drop_percent
FROM drop_calc
ORDER BY usage_drop_percent DESC;

-- 5. Business question: Which OLTs have the highest average congestion?
SELECT
    olt_id,
    AVG(congestion_ratio_percent) AS avg_congestion_ratio_percent,
    DENSE_RANK() OVER (ORDER BY AVG(congestion_ratio_percent) DESC) AS congestion_rank
FROM olt_daily_metrics
GROUP BY olt_id
ORDER BY congestion_rank;

-- 6. Business question: Which customers have poor experience but no recorded complaint?
SELECT
    customer_id,
    log_date,
    experience_score,
    complaint_count,
    churn_risk_score,
    churn_risk_category
FROM customer_daily_metrics
WHERE complaint_leakage_flag = 1
ORDER BY experience_score ASC, churn_risk_score DESC;

-- 7. Business question: Do the headline KPIs match the README?
SELECT
    (SELECT COUNT(DISTINCT customer_id) FROM customers_clean) AS total_customers,
    (SELECT COUNT(DISTINCT customer_id)
     FROM customer_daily_metrics
     WHERE churn_risk_category = 'High Risk') AS high_risk_customers,
    (SELECT AVG(experience_score)
     FROM customer_daily_metrics) AS avg_experience_score,
    (SELECT SUM(complaint_leakage_flag)
     FROM customer_daily_metrics) AS complaint_leakage_count,
    (SELECT AVG(congestion_ratio_percent) FROM olt_daily_metrics) AS avg_congestion_ratio_percent;
