from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "clean"
RAW_DIR = PROJECT_DIR / "data" / "raw"


def add_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["speed_score"] = np.select(
        [out["avg_speed_mbps"] >= 100, out["avg_speed_mbps"].between(50, 99), out["avg_speed_mbps"].between(20, 49)],
        [100, 75, 50],
        default=25,
    )
    out["downtime_score"] = np.select(
        [out["downtime_minutes"].between(0, 10), out["downtime_minutes"].between(11, 30), out["downtime_minutes"].between(31, 60)],
        [100, 75, 50],
        default=25,
    )
    out["latency_score"] = np.select(
        [out["latency_ms"].between(0, 30), out["latency_ms"].between(31, 60), out["latency_ms"].between(61, 100)],
        [100, 75, 50],
        default=25,
    )
    out["experience_score"] = (0.5 * out["speed_score"] + 0.3 * out["downtime_score"] + 0.2 * out["latency_score"]).round(2)
    return out


def main() -> None:
    usage = add_scores(pd.read_csv(DATA_DIR / "usage_logs_clean.csv")).sort_values(["customer_id", "log_date"])
    complaints = pd.read_csv(DATA_DIR / "complaints.csv")
    traffic_path = RAW_DIR / "olt_traffic.xlsx"
    if not traffic_path.exists():
        raise FileNotFoundError("Place olt_traffic.xlsx in data/raw before rerunning metrics.")

    usage["current_7d_avg"] = usage.groupby("customer_id")["data_usage_gb"].transform(lambda s: s.rolling(7, min_periods=1).mean())
    usage["previous_7d_avg"] = usage.groupby("customer_id")["current_7d_avg"].shift(1)
    usage["usage_drop_percent"] = np.where(
        usage["previous_7d_avg"].fillna(0) == 0,
        np.nan,
        ((usage["previous_7d_avg"] - usage["current_7d_avg"]) / usage["previous_7d_avg"]) * 100,
    )

    complaint_counts = complaints.groupby("customer_id").size().rename("complaint_count")
    max_date = pd.to_datetime(usage["log_date"]).max()
    complaints_30 = complaints[pd.to_datetime(complaints["complaint_date"]) >= (max_date - pd.Timedelta(days=30))]
    complaint_counts_30 = complaints_30.groupby("customer_id").size().rename("complaint_count_30d")
    usage = usage.merge(complaint_counts, on="customer_id", how="left").merge(complaint_counts_30, on="customer_id", how="left")
    usage[["complaint_count", "complaint_count_30d"]] = usage[["complaint_count", "complaint_count_30d"]].fillna(0).astype("int64")

    usage["complaint_leakage_flag"] = ((usage["experience_score"] < 50) & (usage["complaint_count"] == 0)).astype("int64")
    usage["high_usage_drop_flag"] = (usage["usage_drop_percent"] >= 30).astype("int64")
    usage["high_downtime_flag"] = (usage["downtime_minutes"] > 20).astype("int64")
    usage["high_latency_flag"] = (usage["latency_ms"] > 40).astype("int64")
    usage["low_experience_flag"] = (usage["experience_score"] < 50).astype("int64")
    usage["churn_risk_score"] = (
        30 * usage["high_usage_drop_flag"]
        + 25 * usage["high_downtime_flag"]
        + 20 * usage["high_latency_flag"]
        + 15 * usage["low_experience_flag"]
        + 10 * usage["complaint_leakage_flag"]
    ).clip(0, 100)
    usage["churn_risk_category"] = pd.cut(usage["churn_risk_score"], bins=[-1, 39, 69, 100], labels=["Low Risk", "Medium Risk", "High Risk"]).astype(str)
    usage.to_csv(DATA_DIR / "customer_daily_metrics.csv", index=False)

    traffic = pd.read_excel(traffic_path)
    traffic["log_date"] = pd.to_datetime(traffic["log_date"]).dt.strftime("%Y-%m-%d")
    traffic["avg_gbps"] = (traffic["total_usage_gb"] * 8) / (24 * 3600)
    traffic["congestion_ratio"] = traffic["avg_gbps"] / traffic["capacity_gbps"]
    traffic["congestion_ratio_percent"] = traffic["congestion_ratio"] * 100
    traffic["congestion_status"] = np.select(
        [traffic["congestion_ratio_percent"] < 60, traffic["congestion_ratio_percent"].between(60, 80)],
        ["Healthy", "Moderate"],
        default="High",
    )
    traffic[
        ["olt_id", "log_date", "total_usage_gb", "capacity_gbps", "avg_gbps", "congestion_ratio", "congestion_ratio_percent", "congestion_status"]
    ].to_csv(DATA_DIR / "olt_daily_metrics.csv", index=False)


if __name__ == "__main__":
    main()
