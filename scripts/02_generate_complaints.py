from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "clean"


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
    out["experience_score"] = 0.5 * out["speed_score"] + 0.3 * out["downtime_score"] + 0.2 * out["latency_score"]
    return out


def main() -> None:
    usage = pd.read_csv(DATA_DIR / "usage_logs_clean.csv")
    usage = add_scores(usage)
    poor = usage[(usage["downtime_minutes"] > 20) | (usage["latency_ms"] > 40) | (usage["experience_score"] < 50)].copy()
    poor_customers = sorted(poor["customer_id"].unique())
    rng = np.random.default_rng(42)
    if not poor_customers:
        poor = usage.sort_values(["downtime_minutes", "latency_ms"], ascending=False).head(max(1, len(usage) // 10)).copy()
        poor_customers = sorted(poor["customer_id"].unique())
    selected = set(rng.choice(poor_customers, size=max(1, int(round(len(poor_customers) * 0.65))), replace=False))

    rows = []
    for i, customer_id in enumerate(sorted(selected), start=1):
        event = poor[poor["customer_id"] == customer_id].sort_values(["downtime_minutes", "latency_ms"], ascending=False).iloc[0]
        if event["downtime_minutes"] > 60:
            category = "outage"
        elif event["latency_ms"] > 80 or event["avg_speed_mbps"] < 50:
            category = "speed"
        else:
            category = "other"
        rows.append(
            {
                "complaint_id": f"CMP_{i:05d}",
                "customer_id": customer_id,
                "complaint_date": event["log_date"],
                "category": category,
                "resolution_time_hours": int(rng.integers(4, 96)),
            }
        )
    pd.DataFrame(rows).to_csv(DATA_DIR / "complaints.csv", index=False)


if __name__ == "__main__":
    main()
