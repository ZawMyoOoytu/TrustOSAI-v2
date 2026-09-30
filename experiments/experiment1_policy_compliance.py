import os
import numpy as np
import pandas as pd


# ============================================================
# TrustOSAI - Experiment 1: Policy Compliance
# ============================================================
#
# Goal:
# Evaluate runtime governance under different levels
# of policy-violating agent behavior.
#
# Systems:
#   1. Conventional Agentic AI
#   2. Static Policy Enforcement
#   3. TrustOSAI
#
# Metrics:
#   PCR = Policy Compliance Rate
#   CAR = Compliant Approval Rate
#   UAR = Unsafe Action Reduction
#
# IMPORTANT:
# The numerical simulation settings below are experimental
# assumptions and are NOT values stated in the paper.
# ============================================================


# ============================================================
# 1. Experiment Configuration
# ============================================================

N_AGENTS = 100
REQUESTS_PER_AGENT = 100

N_REQUESTS = (
    N_AGENTS
    *
    REQUESTS_PER_AGENT
)

N_RUNS = 30


# ------------------------------------------------------------
# Policy violation scenarios
# ------------------------------------------------------------

VIOLATION_LEVELS = {
    "Low": 0.10,
    "Medium": 0.30,
    "High": 0.50,
}


# ------------------------------------------------------------
# TrustOSAI experimental assumptions
# ------------------------------------------------------------

ALPHA = 0.80

T_INITIAL = 0.80

T_MIN = 0.60

R_MAX = 0.70


# ------------------------------------------------------------
# Detection assumptions
# ------------------------------------------------------------

POLICY_DETECTION = 0.95

RISK_DETECTION = 0.90

RISK_GIVEN_VIOLATION = 0.70


# ============================================================
# 2. Output Directory
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_DIR = os.path.dirname(
    BASE_DIR
)

RESULTS_DIR = os.path.join(
    PROJECT_DIR,
    "results",
    "experiment1"
)

os.makedirs(
    RESULTS_DIR,
    exist_ok=True
)


# ============================================================
# 3. Single Simulation Run
# ============================================================

def run_simulation(
    p_violation,
    system,
    seed
):

    rng = np.random.default_rng(seed)

    # --------------------------------------------------------
    # Generate ground-truth actions
    # --------------------------------------------------------

    violation = (
        rng.random(N_REQUESTS)
        <
        p_violation
    )

    # --------------------------------------------------------
    # Assign risk property to violating actions
    # --------------------------------------------------------

    risky = (
        violation
        &
        (
            rng.random(N_REQUESTS)
            <
            RISK_GIVEN_VIOLATION
        )
    )

    # --------------------------------------------------------
    # Initialize decision arrays
    # --------------------------------------------------------

    approved = np.zeros(
        N_REQUESTS,
        dtype=bool
    )

    human_review = np.zeros(
        N_REQUESTS,
        dtype=bool
    )

    unsafe_executed = np.zeros(
        N_REQUESTS,
        dtype=bool
    )


    # ========================================================
    # System A:
    # Conventional Agentic AI
    # ========================================================

    if system == "Conventional Agentic AI":

        # No runtime governance.
        # Every generated action is executed.

        approved[:] = True

        unsafe_executed = (
            violation.copy()
        )


    # ========================================================
    # System B:
    # Static Policy Enforcement
    # ========================================================

    elif system == "Static Policy Enforcement":

        # Static policy detection.

        detected_violation = (
            violation
            &
            (
                rng.random(N_REQUESTS)
                <
                POLICY_DETECTION
            )
        )

        # Actions without detected violations
        # are approved.

        approved = (
            ~detected_violation
        )

        # Unsafe actions that passed
        # the static policy check.

        unsafe_executed = (
            violation
            &
            approved
        )


    # ========================================================
    # System C:
    # TrustOSAI
    # ========================================================

    elif system == "TrustOSAI":

        # Initial dynamic trust score.

        trust = T_INITIAL

        # Process actions sequentially because
        # trust is updated after each action.

        for i in range(N_REQUESTS):

            # ------------------------------------------------
            # Policy validation
            # ------------------------------------------------

            policy_violation_detected = (
                violation[i]
                and
                (
                    rng.random()
                    <
                    POLICY_DETECTION
                )
            )


            # ------------------------------------------------
            # Runtime risk estimation
            # ------------------------------------------------

            risk_detected = (
                risky[i]
                and
                (
                    rng.random()
                    <
                    RISK_DETECTION
                )
            )

            if risk_detected:

                risk = 0.85

            else:

                risk = 0.20


            # ------------------------------------------------
            # Algorithm 1 decision logic
            # ------------------------------------------------

            if (
                not policy_violation_detected
                and
                trust >= T_MIN
                and
                risk <= R_MAX
            ):

                decision = "ALLOW"


            elif (
                not policy_violation_detected
                and
                trust >= T_MIN
                and
                risk > R_MAX
            ):

                decision = "HUMAN_REVIEW"


            elif (
                not policy_violation_detected
                and
                trust < T_MIN
            ):

                decision = "HUMAN_REVIEW"


            else:

                decision = "BLOCK"


            # ------------------------------------------------
            # Store governance decision
            # ------------------------------------------------

            if decision == "ALLOW":

                approved[i] = True


            elif decision == "HUMAN_REVIEW":

                human_review[i] = True


            # ------------------------------------------------
            # Determine unsafe execution
            # ------------------------------------------------

            unsafe_executed[i] = (
                violation[i]
                and
                approved[i]
            )


            # ------------------------------------------------
            # Trust update - Eq. (3)
            #
            # T_new = alpha*T_old + (1-alpha)*Q
            # ------------------------------------------------

            if violation[i]:

                Q = 0.0

            else:

                Q = 1.0


            trust = (
                ALPHA * trust
                +
                (1 - ALPHA) * Q
            )


    else:

        raise ValueError(
            f"Unknown system: {system}"
        )


    # ========================================================
    # 4. Calculate Metrics
    # ========================================================

    total_actions = N_REQUESTS

    unsafe_actions = int(
        violation.sum()
    )

    approved_actions = int(
        approved.sum()
    )

    unsafe_executed_count = int(
        unsafe_executed.sum()
    )

    human_review_count = int(
        human_review.sum()
    )


    # --------------------------------------------------------
    # Blocked unsafe actions
    # --------------------------------------------------------

    blocked_unsafe = int(
        (
            violation
            &
            (~approved)
        ).sum()
    )


    # --------------------------------------------------------
    # Compliant approved actions
    # --------------------------------------------------------

    compliant_approved = int(
        (
            (~violation)
            &
            approved
        ).sum()
    )


    # ========================================================
    # Paper Eq. (4)
    #
    # PCR = N_approved / N_total * 100
    # ========================================================

    PCR = (
        approved_actions
        /
        total_actions
        *
        100
    )


    # ========================================================
    # Additional safety-oriented metric
    #
    # CAR =
    # compliant approved actions / total actions * 100
    # ========================================================

    CAR = (
        compliant_approved
        /
        total_actions
        *
        100
    )


    # ========================================================
    # Paper Eq. (5)
    #
    # UAR = A_blocked / A_unsafe * 100
    # ========================================================

    if unsafe_actions > 0:

        UAR = (
            blocked_unsafe
            /
            unsafe_actions
            *
            100
        )

    else:

        UAR = 100.0


    # ========================================================
    # Return results
    # ========================================================

    return {

        "PCR": PCR,

        "CAR": CAR,

        "UAR": UAR,

        "UnsafeGenerated": unsafe_actions,

        "UnsafeExecuted": unsafe_executed_count,

        "Approved": approved_actions,

        "BlockedUnsafe": blocked_unsafe,

        "HumanReview": human_review_count,

    }


# ============================================================
# 5. Systems
# ============================================================

SYSTEMS = [

    "Conventional Agentic AI",

    "Static Policy Enforcement",

    "TrustOSAI",

]


# ============================================================
# 6. Run Full Experiment
# ============================================================

results = []

seed = 1000


for scenario, p_violation in VIOLATION_LEVELS.items():

    for system in SYSTEMS:

        for run in range(N_RUNS):

            metrics = run_simulation(

                p_violation=p_violation,

                system=system,

                seed=seed

            )

            results.append({

                "Scenario":
                    scenario,

                "ViolationProbability":
                    p_violation,

                "System":
                    system,

                "Run":
                    run + 1,

                **metrics

            })

            seed += 1


# ============================================================
# 7. Convert Results to DataFrame
# ============================================================

results_df = pd.DataFrame(
    results
)


# ============================================================
# 8. Summary Statistics
# ============================================================

summary_df = (

    results_df

    .groupby(
        [
            "Scenario",
            "ViolationProbability",
            "System"
        ]
    )

    .agg(

        PCR_mean=(
            "PCR",
            "mean"
        ),

        PCR_std=(
            "PCR",
            "std"
        ),

        CAR_mean=(
            "CAR",
            "mean"
        ),

        CAR_std=(
            "CAR",
            "std"
        ),

        UAR_mean=(
            "UAR",
            "mean"
        ),

        UAR_std=(
            "UAR",
            "std"
        ),

        UnsafeGenerated_mean=(
            "UnsafeGenerated",
            "mean"
        ),

        UnsafeExecuted_mean=(
            "UnsafeExecuted",
            "mean"
        ),

        BlockedUnsafe_mean=(
            "BlockedUnsafe",
            "mean"
        ),

        HumanReview_mean=(
            "HumanReview",
            "mean"
        )

    )

    .reset_index()

)


# ============================================================
# 9. Save Raw Results
# ============================================================

raw_results_path = os.path.join(
    RESULTS_DIR,
    "raw_results.csv"
)

results_df.to_csv(
    raw_results_path,
    index=False
)


# ============================================================
# 10. Save Summary Results
# ============================================================

summary_results_path = os.path.join(
    RESULTS_DIR,
    "summary_results.csv"
)

summary_df.to_csv(
    summary_results_path,
    index=False
)


# ============================================================
# 11. Display Full Results
# ============================================================

pd.set_option(
    "display.max_columns",
    None
)

pd.set_option(
    "display.width",
    250
)

pd.set_option(
    "display.max_rows",
    None
)


print()
print("=" * 90)
print("TrustOSAI - Experiment 1: Policy Compliance")
print("=" * 90)

print()

print(
    f"Agents              : {N_AGENTS}"
)

print(
    f"Requests / Agent    : {REQUESTS_PER_AGENT}"
)

print(
    f"Total Requests      : {N_REQUESTS}"
)

print(
    f"Simulation Runs     : {N_RUNS}"
)

print(
    f"Alpha               : {ALPHA}"
)

print(
    f"Initial Trust       : {T_INITIAL}"
)

print(
    f"Trust Threshold     : {T_MIN}"
)

print(
    f"Risk Threshold      : {R_MAX}"
)

print()

print("=" * 90)
print("SUMMARY RESULTS")
print("=" * 90)

print()

print(
    summary_df.to_string(
        index=False
    )
)

print()

print("=" * 90)
print("FILES SAVED")
print("=" * 90)

print()

print(
    f"Raw results    : {raw_results_path}"
)

print(
    f"Summary results: {summary_results_path}"
)

print()

print("=" * 90)
print("Experiment 1 completed successfully.")
print("=" * 90)
# ============================================================
# 12. Generate Figures
# ============================================================

import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Figure 1:
# Policy Compliance Rate (PCR)
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for system in SYSTEMS:

    system_data = (
        summary_df[
            summary_df["System"] == system
        ]
        .sort_values("ViolationProbability")
    )

    plt.errorbar(
        system_data["ViolationProbability"],
        system_data["PCR_mean"],
        yerr=system_data["PCR_std"],
        marker="o",
        capsize=4,
        label=system
    )


plt.xlabel(
    "Policy Violation Probability"
)

plt.ylabel(
    "Policy Compliance Rate (%)"
)

plt.title(
    "Experiment 1: Policy Compliance Rate"
)

plt.ylim(
    0,
    105
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()

plt.tight_layout()


figure1_path = os.path.join(
    RESULTS_DIR,
    "figure1_policy_compliance.png"
)

plt.savefig(
    figure1_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# Figure 2:
# Unsafe Executed Actions
# ------------------------------------------------------------

plt.figure(figsize=(9, 6))

for system in SYSTEMS:

    system_data = (
        summary_df[
            summary_df["System"] == system
        ]
        .sort_values("ViolationProbability")
    )

    plt.errorbar(
        system_data["ViolationProbability"],
        system_data["UnsafeExecuted_mean"],
        marker="o",
        capsize=4,
        label=system
    )


plt.xlabel(
    "Policy Violation Probability"
)

plt.ylabel(
    "Mean Unsafe Executed Actions"
)

plt.title(
    "Experiment 1: Unsafe Action Execution"
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()

plt.tight_layout()


figure2_path = os.path.join(
    RESULTS_DIR,
    "figure2_unsafe_actions.png"
)

plt.savefig(
    figure2_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 13. Generate Paper-Ready Main Result Table
# ============================================================

paper_table = summary_df[
    [
        "Scenario",
        "ViolationProbability",
        "System",
        "PCR_mean",
        "PCR_std",
        "CAR_mean",
        "CAR_std",
        "UAR_mean",
        "UAR_std",
        "UnsafeExecuted_mean",
        "HumanReview_mean"
    ]
].copy()


paper_table = paper_table.rename(
    columns={
        "ViolationProbability":
            "Violation Probability",

        "PCR_mean":
            "PCR Mean (%)",

        "PCR_std":
            "PCR SD",

        "CAR_mean":
            "CAR Mean (%)",

        "CAR_std":
            "CAR SD",

        "UAR_mean":
            "UAR Mean (%)",

        "UAR_std":
            "UAR SD",

        "UnsafeExecuted_mean":
            "Unsafe Executed Mean",

        "HumanReview_mean":
            "Human Review Mean"
    }
)


paper_table_path = os.path.join(
    RESULTS_DIR,
    "experiment1_paper_table.csv"
)

paper_table.to_csv(
    paper_table_path,
    index=False
)


# ============================================================
# 14. Final Output
# ============================================================

print()
print("=" * 90)
print("FIGURES AND PAPER TABLE GENERATED")
print("=" * 90)

print()

print(
    f"Figure 1: {figure1_path}"
)

print(
    f"Figure 2: {figure2_path}"
)

print(
    f"Paper table: {paper_table_path}"
)

print()

print("=" * 90)
print("Experiment 1 is ready for result analysis.")
print("=" * 90)