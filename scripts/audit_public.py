"""Reproduce service-experience and data-readiness evidence from public CSVs.

No private source files, Power BI engine or historical churn labels are used.
Outputs contain aggregates, not service-account identifiers.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "clean"


def audit(data_dir: Path = DATA) -> dict:
    names = [
        "customers_clean", "usage_logs_clean", "customer_daily_metrics",
        "olt_daily_metrics", "olt_info_clean", "complaints",
    ]
    d = {name: pd.read_csv(data_dir / f"{name}.csv") for name in names}
    customers, usage, metrics = (d[name] for name in names[:3])
    network, olts, complaints = (d[name] for name in names[3:])
    if customers.customer_id.isna().any() or customers.customer_id.duplicated().any():
        raise ValueError("Customer service-account key must be unique and non-null")
    for frame, label in ((usage, "usage"), (metrics, "metrics")):
        if frame[["customer_id", "log_date"]].isna().any().any() or frame.duplicated(["customer_id", "log_date"]).any():
            raise ValueError(f"Invalid {label} account/date grain")
    if complaints.complaint_id.isna().any() or complaints.complaint_id.duplicated().any():
        raise ValueError("Invalid complaint event key")
    if not usage.customer_id.isin(customers.customer_id).all() or not complaints.customer_id.isin(customers.customer_id).all():
        raise ValueError("Orphan service-account reference")
    if olts.olt_id.isna().any() or olts.olt_id.duplicated().any():
        raise ValueError("Invalid OLT dimension key")
    if not usage.olt_id.isin(olts.olt_id).all():
        raise ValueError("Orphan logged OLT")
    if not customers.olt_id.isin(olts.olt_id).all():
        raise ValueError("Orphan assigned OLT")
    if len(metrics) != len(usage) or set(zip(metrics.customer_id, metrics.log_date)) != set(zip(usage.customer_id, usage.log_date)):
        raise ValueError("Metric and usage account/day keys differ")

    dates = pd.to_datetime(usage.log_date)
    day_counts = usage.groupby("customer_id").log_date.nunique()
    joined = usage.merge(
        customers[["customer_id", "olt_id"]], on="customer_id",
        suffixes=("_logged", "_assigned"), validate="many_to_one"
    )
    mismatch = joined.olt_id_logged.ne(joined.olt_id_assigned)
    mismatched_accounts = int(joined.loc[mismatch, "customer_id"].nunique())
    logged_olts = set(usage.olt_id)
    missing_olts = sorted(set(olts.olt_id) - logged_olts)
    if not metrics.usage_window_complete.fillna(False).any() and metrics.churn_risk_score.notna().any():
        raise ValueError("A full risk score is present without a complete usage window")

    # Rebuild daily-average ratios from source usage and supplied capacity.
    rebuilt = usage.groupby(["olt_id", "log_date"], as_index=False).data_usage_gb.sum()
    rebuilt = rebuilt.merge(olts[["olt_id", "capacity_gbps"]], on="olt_id", validate="many_to_one")
    if rebuilt.capacity_gbps.isna().any() or rebuilt.capacity_gbps.le(0).any():
        raise ValueError("Invalid supplied OLT capacity")
    rebuilt["expected_ratio"] = rebuilt.data_usage_gb * 8 / 86400 / rebuilt.capacity_gbps
    paired = rebuilt.merge(network[["olt_id", "log_date", "congestion_ratio"]], on=["olt_id", "log_date"], validate="one_to_one")
    if len(paired) != len(network) or not np.allclose(paired.expected_ratio, paired.congestion_ratio, atol=1e-12):
        raise ValueError("Network daily-average ratio does not reconcile")

    by_assigned = joined.groupby("olt_id_assigned").customer_id.nunique().rename("service_accounts").to_frame()
    by_assigned["mismatched_accounts"] = (
        joined.loc[mismatch].groupby("olt_id_assigned").customer_id.nunique()
    ).reindex(by_assigned.index, fill_value=0)
    by_assigned = by_assigned.reset_index()
    receipt = {
        "scope": "committed Excel-generated usage simulation; private customer-source metadata; complaints synthetic",
        "usage_classification": "synthetic, confirmed by project author",
        "account_id_strategy": "generated sequential row labels; frozen sample/order only",
        "olt_scope_interpretation": "ten simulated usage IDs versus twelve source-address groups; not verified physical inventory",
        "service_accounts": int(len(customers)),
        "account_days": int(len(usage)),
        "date_start": dates.min().strftime("%Y-%m-%d"),
        "date_end": dates.max().strftime("%Y-%m-%d"),
        "distinct_dates": int(dates.nunique()),
        "days_per_account_min": int(day_counts.min()),
        "days_per_account_max": int(day_counts.max()),
        "complete_14_day_window_rows": int(metrics.usage_window_complete.fillna(False).sum()),
        "full_risk_score_rows": int(metrics.churn_risk_score.notna().sum()),
        "unavailable_risk_rows": int(metrics.churn_risk_score.isna().sum()),
        "total_olt_groups": int(len(olts)),
        "observed_logged_olt_groups": int(len(logged_olts)),
        "missing_logged_olt_ids": [int(v) for v in missing_olts],
        "assigned_logged_mismatched_accounts": mismatched_accounts,
        "assigned_logged_mismatch_share": float(mismatched_accounts / len(customers)),
        "assigned_logged_mismatched_account_days": int(mismatch.sum()),
        "mismatch_by_assigned_olt": [
            {"assigned_olt_id": int(r.olt_id_assigned), "service_accounts": int(r.service_accounts),
             "mismatched_accounts": int(r.mismatched_accounts)}
            for r in by_assigned.itertuples()
        ],
        "mean_daily_average_utilization_decimal": float(network.congestion_ratio.mean()),
        "maximum_observed_daily_average_utilization_decimal": float(network.congestion_ratio.max()),
        "mean_experience_score": float(metrics.experience_score.mean()),
        "synthetic_complaint_events": int(len(complaints)),
        "complaint_leakage_account_keys": int(metrics.loc[metrics.complaint_leakage_flag.eq(1), "customer_id"].nunique()),
        "peak_throughput": "not observed; input usage is synthetic",
        "historical_churn_outcome": "not available",
        "power_bi_execution": "not verified by this Python/SQLite audit",
    }
    with sqlite3.connect(":memory:") as db:
        customers.to_sql("customers", db, index=False)
        usage.to_sql("usage", db, index=False)
        sql_mismatch = db.execute("""
            SELECT COUNT(DISTINCT c.customer_id) FROM customers c
            JOIN usage u USING(customer_id) WHERE c.olt_id <> u.olt_id
        """).fetchone()[0]
        sql_observed = db.execute("SELECT COUNT(DISTINCT olt_id) FROM usage").fetchone()[0]
        if (sql_mismatch, sql_observed) != (mismatched_accounts, len(logged_olts)):
            raise ValueError("Python/SQLite mismatch or coverage disagreement")
    receipt["independent_sql_reconciliation"] = "passed for mismatch and observed OLT coverage"
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Optional aggregate JSON receipt")
    args = parser.parse_args()
    result = audit()
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
