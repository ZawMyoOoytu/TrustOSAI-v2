"""
TrustOSAI Experiment 3
Runtime Governance Overhead

Purpose:
    Evaluate the runtime overhead introduced by TrustOSAI governance
    compared with conventional execution.

Metric:
    O_g = ((T_g - T_e) / T_e) * 100

This experiment uses a simulation-based latency model.
It does not represent measurements from real hardware or deployment.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Configuration
# ============================================================

N_RUNS = 30
N_REQUESTS = 1000

# Simulated baseline execution latency (milliseconds)
BASE_EXECUTION_MEAN_MS = 100.0
BASE_EXECUTION_SD_MS = 10.0

# Simulated governance processing components (milliseconds)
POLICY_CHECK_MEAN_MS = 5.0
POLICY_CHECK_SD_MS = 1.0

TRUST_ASSESSMENT_MEAN_MS = 3.0
TRUST_ASSESSMENT_SD_MS = 0.8

RISK_ASSESSMENT_MEAN_MS = 4.0
RISK_ASSESSMENT_SD_MS = 1.0

DECISION_ENGINE_MEAN_MS = 2.0
DECISION_ENGINE_SD_MS = 0.5

OUTPUT_DIR = Path("results/experiment3")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Simulation
# ============================================================

def run_simulation(seed):
    rng = np.random.default_rng(seed)

    records = []

    for request_id in range(1, N_REQUESTS + 1):

        # Baseline execution latency
        execution_time = max(
            1.0,
            rng.normal(
                BASE_EXECUTION_MEAN_MS,
                BASE_EXECUTION_SD_MS
            )
        )

        # Governance processing latency
        policy_check = max(
            0.0,
            rng.normal(
                POLICY_CHECK_MEAN_MS,
                POLICY_CHECK_SD_MS
            )
        )

        trust_assessment = max(
            0.0,
            rng.normal(
                TRUST_ASSESSMENT_MEAN_MS,
                TRUST_ASSESSMENT_SD_MS
            )
        )

        risk_assessment = max(
            0.0,
            rng.normal(
                RISK_ASSESSMENT_MEAN_MS,
                RISK_ASSESSMENT_SD_MS
            )
        )

        decision_engine = max(
            0.0,
            rng.normal(
                DECISION_ENGINE_MEAN_MS,
                DECISION_ENGINE_SD_MS
            )
        )

        governance_overhead = (
            policy_check
            + trust_assessment
            + risk_assessment
            + decision_engine
        )

        governed_execution = execution_time + governance_overhead

        overhead_percent = (
            (governed_execution - execution_time)
            / execution_time
        ) * 100.0

        records.append({
            "Run": seed,
            "Request": request_id,
            "Execution_Time_ms": execution_time,
            "Policy_Check_ms": policy_check,
            "Trust_Assessment_ms": trust_assessment,
            "Risk_Assessment_ms": risk_assessment,
            "Decision_Engine_ms": decision_engine,
            "Governance_Overhead_ms": governance_overhead,
            "Governed_Execution_ms": governed_execution,
            "Governance_Overhead_Percent": overhead_percent,
        })

    return pd.DataFrame(records)


# ============================================================
# Run experiments
# ============================================================

all_results = []

for run in range(1, N_RUNS + 1):
    df_run = run_simulation(run)
    all_results.append(df_run)

raw_results = pd.concat(all_results, ignore_index=True)


# ============================================================
# Summary
# ============================================================

summary = pd.DataFrame({
    "Metric": [
        "Baseline Execution Time (ms)",
        "Governed Execution Time (ms)",
        "Governance Overhead (ms)",
        "Governance Overhead (%)",
    ],
    "Mean": [
        raw_results["Execution_Time_ms"].mean(),
        raw_results["Governed_Execution_ms"].mean(),
        raw_results["Governance_Overhead_ms"].mean(),
        raw_results["Governance_Overhead_Percent"].mean(),
    ],
    "SD": [
        raw_results["Execution_Time_ms"].std(),
        raw_results["Governed_Execution_ms"].std(),
        raw_results["Governance_Overhead_ms"].std(),
        raw_results["Governance_Overhead_Percent"].std(),
    ],
})


# ============================================================
# Save results
# ============================================================

raw_results.to_csv(
    OUTPUT_DIR / "raw_results.csv",
    index=False
)

summary.to_csv(
    OUTPUT_DIR / "summary_results.csv",
    index=False
)


# ============================================================
# Figure 5: Execution Latency Comparison
# ============================================================

baseline_mean = raw_results["Execution_Time_ms"].mean()
governed_mean = raw_results["Governed_Execution_ms"].mean()

plt.figure(figsize=(8, 5))

plt.bar(
    ["Baseline Execution", "TrustOSAI Governed"],
    [baseline_mean, governed_mean]
)

plt.ylabel("Latency (ms)")
plt.title("Figure 5. Execution Latency Comparison")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "figure5_execution_latency.png",
    dpi=300
)

plt.close()


# ============================================================
# Figure 6: Governance Overhead Distribution
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    raw_results["Governance_Overhead_Percent"],
    bins=30
)

plt.xlabel("Governance Overhead (%)")
plt.ylabel("Frequency")
plt.title("Figure 6. Governance Runtime Overhead Distribution")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "figure6_governance_overhead.png",
    dpi=300
)

plt.close()


# ============================================================
# Console output
# ============================================================

print("=" * 60)
print("TrustOSAI Experiment 3")
print("Runtime Governance Overhead")
print("=" * 60)

print()
print(summary.to_string(index=False))

print()
print("Output files:")
print(f"  {OUTPUT_DIR / 'raw_results.csv'}")
print(f"  {OUTPUT_DIR / 'summary_results.csv'}")
print(f"  {OUTPUT_DIR / 'figure5_execution_latency.png'}")
print(f"  {OUTPUT_DIR / 'figure6_governance_overhead.png'}")

print()
print("Experiment 3 completed successfully.")
print("Note: These are simulation-based latency results,")
print("not measurements from real hardware or deployment.")