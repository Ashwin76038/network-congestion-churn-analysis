from __future__ import annotations

from pathlib import Path
import pandas as pd

SOURCE_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "clean"


def normalize_id(value: object) -> str:
    return f"Customer_{int(value):05d}"


def value_to_plan_tier(value_segment: str) -> str:
    return {"free_plan": "Free", "low_value": "Basic", "mid_value": "Standard", "high_value": "Premium"}.get(str(value_segment), "Standard")


def value_to_plan_id(value_segment: str) -> int:
    return {"free_plan": 1, "low_value": 2, "mid_value": 3, "high_value": 4}.get(str(value_segment), 3)


def extract_area(address: object) -> str:
    if pd.isna(address):
        return "Unknown"
    text = str(address).upper()
    tokens = [t.strip(" .") for t in text.split(",") if t.strip(" .")]
    for token in tokens:
        if token in {"COIMBATORE", "METTUPALAYAM"}:
            return token.title()
    return "Unknown"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    customers = pd.read_excel(SOURCE_DIR / "customers.xlsx")
    usage = pd.read_csv(SOURCE_DIR / "usage_logs.csv")
    plans = pd.read_csv(SOURCE_DIR / "plans.csv")
    olt = pd.read_csv(SOURCE_DIR / "olt_info.csv")

    id_map = {raw_id: normalize_id(raw_id) for raw_id in customers["customer_id"]}
    olt_map = dict(zip(olt["olt_ip"], olt["olt_id"]))

    customers_clean = pd.DataFrame(
        {
            "customer_id": customers["customer_id"].map(id_map),
            "plan_id": customers["plan_category"].map(value_to_plan_id).astype("int64"),
            "olt_id": customers["OLT IP"].map(olt_map).astype("int64"),
            "activation_date": pd.NA,
            "activation_date_withheld_flag": 1,
            "legacy_prepared_future_activation_flag": pd.to_datetime(customers["activation date"], dayfirst=True, errors="raise").gt(pd.Timestamp("2026-09-12")).astype(int),
            "status": customers["status"].astype(str).str.lower().str.strip(),
            "customer_type": customers["customer_type"].astype(str).str.lower().str.strip(),
            "connection_count_per_customer": pd.to_numeric(customers["connection_count_per_customer"], errors="coerce").fillna(1).astype("int64"),
            "plan_tier": customers["plan_category"].map(value_to_plan_tier),
            "value_segment": customers["plan_category"].astype(str).str.strip(),
            "area": customers["address"].map(extract_area),
        }
    )

    plans_clean = plans.rename(columns={"plan_name": "plan_tier"}).copy()
    plans_clean["value_segment"] = plans_clean["plan_tier"].map(
        {"Free": "free_plan", "Basic": "low_value", "Standard": "mid_value", "Premium": "high_value"}
    )
    plans_clean = plans_clean[["plan_id", "plan_tier", "value_segment", "speed_mbps", "monthly_price"]]

    usage_clean = usage.copy()
    usage_clean["customer_id"] = usage_clean["customer_id"].map(id_map)
    usage_clean["log_date"] = pd.to_datetime(usage_clean["log_date"], format="%d-%m-%Y", errors="coerce").dt.strftime("%Y-%m-%d")
    usage_clean["value_segment"] = usage_clean["plan_category"].astype(str)
    usage_clean["plan_tier"] = usage_clean["value_segment"].map(value_to_plan_tier)
    usage_clean = usage_clean.drop(columns=["plan_category"])
    usage_clean = usage_clean[
        ["customer_id", "olt_id", "log_date", "plan_tier", "value_segment", "data_usage_gb", "avg_speed_mbps", "downtime_minutes", "latency_ms"]
    ]

    olt_clean = olt.copy()
    olt_clean["olt_name"] = olt_clean["olt_id"].map(lambda x: f"OLT_{int(x):02d}")
    olt_clean = olt_clean[["olt_id", "olt_name", "capacity_gbps"]]

    customers_clean.to_csv(OUTPUT_DIR / "customers_clean.csv", index=False)
    plans_clean.to_csv(OUTPUT_DIR / "plans_clean.csv", index=False)
    usage_clean.to_csv(OUTPUT_DIR / "usage_logs_clean.csv", index=False)
    olt_clean.to_csv(OUTPUT_DIR / "olt_info_clean.csv", index=False)


if __name__ == "__main__":
    main()
