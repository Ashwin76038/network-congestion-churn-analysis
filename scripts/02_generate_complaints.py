from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "clean"


from metrics import add_scores


def main() -> None:
    usage = pd.read_csv(DATA_DIR / "usage_logs_clean.csv")
    usage = add_scores(usage)
    poor = usage[(usage["downtime_minutes"] > 20) | (usage["latency_ms"] > 40) | (usage["experience_score"] < 50)].copy()
    poor_customers = sorted(poor["customer_id"].unique())
    rng = np.random.default_rng(42)
    if not poor_customers:
        pd.DataFrame(columns=["complaint_id","customer_id","complaint_date","category","resolution_time_hours"]).to_csv(DATA_DIR / "complaints.csv", index=False)
        return
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
