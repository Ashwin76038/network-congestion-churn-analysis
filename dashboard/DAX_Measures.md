# DAX Measures

Core measures are preserved. The following definitions are loaded in the Professional semantic model.

## Total Customers

```dax
Total Customers = DISTINCTCOUNT(customers_clean[customer_id])
```

## High Risk Customers

```dax
High Risk Customers = COALESCE(CALCULATE(DISTINCTCOUNT(customer_daily_metrics[customer_id]), KEEPFILTERS(customer_daily_metrics[churn_risk_category] = "High Risk")),0)
```

## % High Risk Customers

```dax
% High Risk Customers = DIVIDE([High Risk Customers],[Total Customers],0)
```

## Avg Experience Score

```dax
Avg Experience Score = AVERAGE(customer_daily_metrics[experience_score])
```

## Complaint Leakage Customers

```dax
Complaint Leakage Customers = COALESCE(CALCULATE(DISTINCTCOUNT(customer_daily_metrics[customer_id]),KEEPFILTERS(customer_daily_metrics[complaint_leakage_flag]=1)),0)
```

## Leakage Rate

```dax
Leakage Rate = DIVIDE([Complaint Leakage Customers],[Total Customers],0)
```

## Avg Congestion Ratio

```dax
Avg Congestion Ratio = AVERAGE(olt_daily_metrics[congestion_ratio_percent])
```

## High Congestion OLTs

```dax
High Congestion OLTs = COALESCE(CALCULATE(DISTINCTCOUNT(olt_daily_metrics[olt_id]),olt_daily_metrics[congestion_status]="High"),0)
```

## Total OLTs

```dax
Total OLTs = DISTINCTCOUNT(olt_info_clean[olt_id])
```

## Monitored OLTs

```dax
Monitored OLTs = DISTINCTCOUNT(olt_daily_metrics[olt_id])
```

## Network Coverage

```dax
Network Coverage = DIVIDE([Monitored OLTs],[Total OLTs],0)
```

## Risk Customers

```dax
Risk Customers = DISTINCTCOUNT(customer_daily_metrics[customer_id])
```

## Risk Summary

```dax
Risk Summary = FORMAT([High Risk Customers],"#,0") & " customers with high-risk observations (" & FORMAT([% High Risk Customers],"0.0%") & ")."
```

## Leakage Status

```dax
Leakage Status = IF([Complaint Leakage Customers]=0,"No Complaint Leakage Cases Detected",FORMAT([Complaint Leakage Customers],"#,0") & " customers need proactive outreach")
```

## Average Throughput Gbps

```dax
Average Throughput Gbps = AVERAGE(olt_daily_metrics[avg_gbps])
```

## Capacity Gbps

```dax
Capacity Gbps = MAX(olt_info_clean[capacity_gbps])
```

## Leakage Experience

```dax
Leakage Experience = CALCULATE(AVERAGE(customer_daily_metrics[experience_score]),customer_daily_metrics[complaint_leakage_flag]=1)
```

## Leakage Risk Score

```dax
Leakage Risk Score = CALCULATE(MAX(customer_daily_metrics[churn_risk_score]),customer_daily_metrics[complaint_leakage_flag]=1)
```

## Avg Downtime Minutes

```dax
Avg Downtime Minutes = AVERAGE(customer_daily_metrics[downtime_minutes])
```

## Avg Latency Ms

```dax
Avg Latency Ms = AVERAGE(customer_daily_metrics[latency_ms])
```

## Avg Risk Score

```dax
Avg Risk Score = AVERAGE(customer_daily_metrics[churn_risk_score])
```

## Max Risk Score

```dax
Max Risk Score = MAX(customer_daily_metrics[churn_risk_score])
```

## Total Usage GB

```dax
Total Usage GB = SUM(usage_logs_clean[data_usage_gb])
```

## Utilization Status

```dax
Utilization Status = VAR R=[Avg Congestion Ratio] RETURN IF(ISBLANK(R),"No telemetry",SWITCH(TRUE(),R<0.6,"Healthy",R<=0.8,"Moderate","High"))
```

## Utilization Color

```dax
Utilization Color = VAR R=[Avg Congestion Ratio] RETURN IF(ISBLANK(R),"#94A3B8",SWITCH(TRUE(),R<0.6,"#149C8B",R<=0.8,"#E5A028","#D94668"))
```

## Network Coverage Summary

```dax
Network Coverage Summary = FORMAT([Monitored OLTs],"0") & " / " & FORMAT([Total OLTs],"0") & " OLTs monitored | 24h average estimate; peak congestion unavailable"
```

## Executive Insight

```dax
Executive Insight = FORMAT([High Risk Customers],"0") & " customers had high-risk observations. " & FORMAT([Complaint Leakage Customers],"0") & " complaint leakage cases in the selected period."
```

## Worst Risk Customers

```dax
Worst Risk Customers = VAR Category = SELECTEDVALUE(customer_daily_metrics[churn_risk_category]) VAR PerCustomer = CALCULATETABLE(SUMMARIZE(customer_daily_metrics,customer_daily_metrics[customer_id],"Worst",MAX(customer_daily_metrics[churn_risk_score])),ALLSELECTED(customer_daily_metrics[churn_risk_category])) RETURN COUNTROWS(FILTER(PerCustomer,SWITCH(TRUE(),[Worst]>=70,"High Risk",[Worst]>=40,"Medium Risk","Low Risk")=Category))
```

Worst Risk Customers prevents double counting across daily risk categories. It evaluates each customer's maximum risk score within the selected dates and slicer context. Network metrics use daily average utilization; they do not measure peak congestion.