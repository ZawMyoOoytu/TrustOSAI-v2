import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# Experiment 2: Trust Evolution and Stability
# ============================================================

# Output directory
RESULTS_DIR = "results/experiment2"
os.makedirs(RESULTS_DIR, exist_ok=True)


# ------------------------------------------------------------
# Frozen parameters reused from Experiment 1
# ------------------------------------------------------------

ALPHA = 0.80
T_INITIAL = 0.80
T_MIN = 0.60

# Experiment 2 parameters
N_INTERACTIONS = 100
N_RUNS = 30

VIOLATION_LEVELS = {
    "Low": 0.10,
    "Medium": 0.30,
    "High": 0.50,
}


# ------------------------------------------------------------
# Trust update
# ------------------------------------------------------------

def update_trust(trust_old, q):
    """
    Equation (3):

        T_new = alpha * T_old + (1-alpha) * Q
    """
    return ALPHA * trust_old + (1 - ALPHA) * q


# ------------------------------------------------------------
# Single simulation
# ------------------------------------------------------------

def run_simulation(p_violation, seed):

    rng = np.random.default_rng(seed)

    trust = T_INITIAL

    records = []

    for interaction in range(1, N_INTERACTIONS + 1):

        # Generate behavioral outcome
        violation = rng.random() < p_violation

        if violation:
            q = 0.0
            behavior = "Violation"
        else:
            q = 1.0
            behavior = "Compliant"

        # Update trust
        trust_previous = trust

        trust = update_trust(
            trust_previous,
            q
        )

        # Governance state
        if trust >= T_MIN:
            decision = "ALLOW"
        else:
            decision = "HUMAN_REVIEW"

        records.append({
            "Interaction": interaction,
            "Trust_Previous": trust_previous,
            "Q": q,
            "Behavior": behavior,
            "Trust": trust,
            "Decision": decision,
            "Violation": int(violation),
        })

    return pd.DataFrame(records)


# ------------------------------------------------------------
# Run all scenarios
# ------------------------------------------------------------

all_results = []

for scenario, p_violation in VIOLATION_LEVELS.items():

    for run in range(1, N_RUNS + 1):

        seed = 1000 + run

        df = run_simulation(
            p_violation=p_violation,
            seed=seed
        )

        df["Scenario"] = scenario
        df["Violation Probability"] = p_violation
        df["Run"] = run

        all_results.append(df)


raw_results = pd.concat(
    all_results,
    ignore_index=True
)


# ------------------------------------------------------------
# Stability metrics
# ------------------------------------------------------------

summary_records = []

for scenario, group in raw_results.groupby("Scenario"):

    # Trust values during final 20 interactions
    final_window = group[
        group["Interaction"] > N_INTERACTIONS - 20
    ]

    final_trust_mean = final_window["Trust"].mean()
    final_trust_std = final_window["Trust"].std()

    overall_trust_mean = group["Trust"].mean()
    overall_trust_std = group["Trust"].std()

    allow_rate = (
        (group["Decision"] == "ALLOW").mean() * 100
    )

    human_review_rate = (
        (group["Decision"] == "HUMAN_REVIEW").mean() * 100
    )

    summary_records.append({
        "Scenario": scenario,
        "Violation Probability":
            group["Violation Probability"].iloc[0],
        "Final Trust Mean": final_trust_mean,
        "Final Trust SD": final_trust_std,
        "Overall Trust Mean": overall_trust_mean,
        "Overall Trust SD": overall_trust_std,
        "ALLOW Rate (%)": allow_rate,
        "Human Review Rate (%)": human_review_rate,
    })


summary = pd.DataFrame(summary_records)


# ------------------------------------------------------------
# Save CSV results
# ------------------------------------------------------------

raw_path = os.path.join(
    RESULTS_DIR,
    "raw_results.csv"
)

summary_path = os.path.join(
    RESULTS_DIR,
    "summary_results.csv"
)

raw_results.to_csv(
    raw_path,
    index=False
)

summary.to_csv(
    summary_path,
    index=False
)


# ------------------------------------------------------------
# Figure 3: Trust Evolution
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

for scenario in VIOLATION_LEVELS:

    scenario_data = raw_results[
        raw_results["Scenario"] == scenario
    ]

    mean_trust = (
        scenario_data
        .groupby("Interaction")["Trust"]
        .mean()
    )

    plt.plot(
        mean_trust.index,
        mean_trust.values,
        label=scenario
    )


plt.axhline(
    T_MIN,
    linestyle="--",
    label="Trust Threshold"
)

plt.xlabel("Interaction Number")
plt.ylabel("Trust Score")
plt.title("Trust Evolution Across Sequential Interactions")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

figure3_path = os.path.join(
    RESULTS_DIR,
    "figure3_trust_evolution.png"
)

plt.savefig(
    figure3_path,
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Figure 4: Governance Decision Distribution
# ------------------------------------------------------------

decision_summary = (
    raw_results
    .groupby(["Scenario", "Decision"])
    .size()
    .reset_index(name="Count")
)

pivot_decisions = decision_summary.pivot(
    index="Scenario",
    columns="Decision",
    values="Count"
).fillna(0)


pivot_decisions.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.xlabel("Scenario")
plt.ylabel("Number of Decisions")
plt.title("Governance Decisions During Trust Evolution")
plt.xticks(rotation=0)
plt.tight_layout()

figure4_path = os.path.join(
    RESULTS_DIR,
    "figure4_governance_decisions.png"
)

plt.savefig(
    figure4_path,
    dpi=300
)

plt.close()


# ------------------------------------------------------------
# Print results
# ------------------------------------------------------------

print("\n==============================================")
print("Experiment 2: Trust Evolution and Stability")
print("==============================================\n")

print(summary.to_string(index=False))

print("\nSaved files:")
print(raw_path)
print(summary_path)
print(figure3_path)
print(figure4_path)

print("\nExperiment 2 completed successfully.")