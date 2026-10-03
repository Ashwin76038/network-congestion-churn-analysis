"""Read a private source workbook and emit aggregate reconciliation only.

No raw rows, names, contact fields, OLT addresses or source workbook are written.
Public dates are compared by source order only after other fields corroborate it.
This script never rebuilds either project's data or Power BI files.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SCOPE = "BHARAT FIBER COMBO"
STATUS_MAPPING = {"A": "active", "D": "partial_active", "E": "inactive"}


def parse_activation(values: pd.Series) -> pd.Series:
    """The supplied original workbook stores DD/MM/YYYY HH:MM:SS strings."""
    parsed = pd.to_datetime(values, format="%d/%m/%Y %H:%M:%S", errors="coerce")
    if parsed.isna().any():
        raise ValueError("Missing or invalid original activation dates; no date inferred")
    return parsed.dt.normalize()


def reconcile(source_path: Path, root: Path = ROOT, as_of: str = "2026-09-12") -> dict:
    raw = pd.read_excel(source_path, sheet_name="sheet1").dropna(how="all")
    required = {"Sub Service Type", "Customer", "OLT IP", "Activation Date", "Status", "FMC", "Subscription Plan"}
    if not required.issubset(raw.columns):
        raise ValueError("Original workbook schema is missing required fields")
    all_dates = parse_activation(raw["Activation Date"])
    source = raw.loc[raw["Sub Service Type"].eq(SCOPE)].reset_index(drop=True)
    if source.empty:
        raise ValueError("No rows in the documented project scope")
    dates = parse_activation(source["Activation Date"])
    cutoff = pd.Timestamp(as_of).normalize()
    names = source.Customer.astype("string").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    source_olt = pd.Series(pd.factorize(source["OLT IP"].astype("string").str.strip().str.lower(), sort=False)[0] + 1)
    expected_status = source.Status.map(STATUS_MAPPING)
    model = root / "data/powerbi_star_schema"
    checks = {}
    if (model / "fact_customer_service.csv").exists():
        public = pd.read_csv(model / "fact_customer_service.csv").sort_values("service_snapshot_key").reset_index(drop=True)
        public = public.merge(pd.read_csv(model / "dim_service_state.csv")[["service_state_key", "service_status"]], on="service_state_key", validate="many_to_one")
        public = public.merge(pd.read_csv(model / "dim_plan.csv")[["plan_key", "subscription_plan"]], on="plan_key", validate="many_to_one")
        public_dates = pd.to_datetime(public.reported_activation_date_key.astype("Int64").astype("string"), format="%Y%m%d")
        project = "olt_service_snapshot"
        if len(source) == len(public):
            checks["listed_fee_rows_matching"] = int(pd.to_numeric(source.FMC, errors="coerce").eq(public.monthly_fee).sum())
            checks["subscription_plan_rows_matching"] = int(source["Subscription Plan"].astype("string").str.strip().eq(public.subscription_plan.astype("string").str.strip()).sum())
            expected_customer = pd.Series([f"CUST_{n + 1:04d}" for n in pd.factorize(names, sort=False)[0]])
            checks["customer_group_sequence_rows_matching"] = int(expected_customer.eq(public.customer_key).sum())
            checks["olt_group_sequence_rows_matching"] = int(source_olt.map(lambda n: f"OLT_{n:04d}").eq(public.olt_key).sum())
            checks["status_mapping_rows_matching"] = int(expected_status.eq(public.service_status).sum())
    else:
        public = pd.read_csv(root / "data/clean/customers_clean.csv").sort_values("customer_id").reset_index(drop=True)
        public_dates = pd.to_datetime(public.activation_date, format="%Y-%m-%d")
        project = "network_service_accounts"
        if len(source) == len(public):
            checks["olt_group_sequence_rows_matching"] = int(source_olt.eq(public.olt_id).sum())
            checks["status_mapping_rows_matching"] = int(expected_status.eq(public.status).sum())
            checks["account_sequence_rows_matching"] = int(pd.Series([f"Customer_{n:05d}" for n in range(1, len(source) + 1)]).eq(public.customer_id).sum())
    corroborated = bool(checks) and len(source) == len(public) and all(v == len(source) for v in checks.values())
    comparable = public_dates.notna()
    matches = int((dates.eq(public_dates) & comparable).sum()) if corroborated and comparable.any() else None
    temporal_checks = {}
    if project == "network_service_accounts" and corroborated:
        usage = pd.read_csv(root / "data/clean/usage_logs_clean.csv")
        source_dates = pd.DataFrame({"customer_id": public.customer_id, "source_activation": dates})
        paired = usage.merge(source_dates, on="customer_id", validate="many_to_one")
        logged = pd.to_datetime(paired.log_date, format="%Y-%m-%d")
        before = logged.lt(paired.source_activation)
        temporal_checks = {
            "account_days_before_source_activation": int(before.sum()),
            "accounts_with_logs_before_source_activation": int(paired.loc[before, "customer_id"].nunique()),
            "source_activations_after_usage_end": int(dates.gt(logged.max()).sum()),
            "usage_classification": "synthetic Excel random values, confirmed by project author",
            "limit": "synthetic dates compared with original activation by corroborated source order; no evidence of real pre-activation traffic",
        }
    return {
        "project": project,
        "source": "private original workbook supplied by project author, who identifies a confidential government-platform export",
        "activation_definition": "project author confirms date internet plan/service was activated",
        "workbook_service_rows": int(len(raw)),
        "source_scope": SCOPE,
        "selected_service_rows": int(len(source)),
        "excluded_other_service_type_rows": int(len(raw) - len(source)),
        "normalized_customer_label_groups": int(names.nunique()),
        "normalization_rule": "trim, lowercase, collapse internal whitespace",
        "source_olt_groups": int(source["OLT IP"].nunique()),
        "workbook_activation_min": all_dates.min().strftime("%Y-%m-%d"),
        "workbook_activation_max": all_dates.max().strftime("%Y-%m-%d"),
        "selected_activation_min": dates.min().strftime("%Y-%m-%d"),
        "selected_activation_max": dates.max().strftime("%Y-%m-%d"),
        "comparison_as_of": cutoff.strftime("%Y-%m-%d"),
        "comparison_as_of_provenance": "current analyst-configured reference date; actual source snapshot date undisclosed",
        "source_future_activation_rows": int(dates.gt(cutoff).sum()),
        "public_service_rows": int(len(public)),
        "public_activation_min": public_dates.min().strftime("%Y-%m-%d") if comparable.any() else None,
        "public_activation_max": public_dates.max().strftime("%Y-%m-%d") if comparable.any() else None,
        "public_activation_dates_available": int(comparable.sum()),
        "public_activation_dates_unavailable": int((~comparable).sum()),
        "public_future_activation_rows": int(public_dates.gt(cutoff).sum()),
        "row_order_corroboration": checks,
        "row_order_corroborated": corroborated,
        "positional_activation_matches": matches,
        "positional_activation_mismatches": int(comparable.sum() - matches) if matches is not None else None,
        "network_usage_temporal_checks": temporal_checks,
        "comparison_limit": "source-order comparison, not a verified stable service-ID join; A/D/E mapping is an analytical assumption because portal definitions are undisclosed",
        "olt_group_limit": "source-address groups, not verified physical inventory; ten separate usage IDs chosen for Network simulation",
        "public_data_changed": False,
        "power_bi_execution": "not executed",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="Private original XLSX; never commit it")
    parser.add_argument("--as-of", default="2026-09-12", help="Comparison cutoff, not an inferred source snapshot date")
    parser.add_argument("--output", type=Path, help="Optional aggregate JSON receipt")
    args = parser.parse_args()
    serialized = json.dumps(reconcile(args.source, as_of=args.as_of), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
