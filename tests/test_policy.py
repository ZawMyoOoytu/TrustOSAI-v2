from engines.policy_engine import PolicyEngine


def test_policy_passes_safe_request():
    engine = PolicyEngine()

    passed, metadata = engine.check_constraints({
        "task": "summarize this document",
        "trust_score": 80,
        "risk_score": 0.10,
        "user_role": "user-default-01",
    })

    assert passed is True
    assert metadata["policy_status"] == "APPROVED"
    assert metadata["governance_level"] == "SAFE"
    assert metadata["violations"] == []


def test_policy_blocks_low_trust():
    engine = PolicyEngine()

    passed, metadata = engine.check_constraints({
        "task": "summarize this document",
        "trust_score": 20,
        "risk_score": 0.10,
        "user_role": "user-default-01",
    })

    assert passed is False
    assert metadata["policy_status"] == "REJECTED"
    assert any(
        v["type"] == "TRUST_THRESHOLD"
        for v in metadata["violations"]
    )


def test_policy_normalizes_percentage_risk():
    engine = PolicyEngine()

    assert engine.normalize_risk(50) == 0.5
    assert engine.normalize_risk(0.5) == 0.5
    assert engine.normalize_risk(150) == 1.0


def test_policy_enforces_rbac_for_write():
    engine = PolicyEngine()

    passed, metadata = engine.check_constraints({
        "task": "delete this record",
        "trust_score": 90,
        "risk_score": 0.10,
        "user_role": "guest",
    })

    assert passed is False
    assert any(
        v["type"] == "RBAC_POLICY"
        for v in metadata["violations"]
    )


def test_policy_detects_blacklisted_topic():
    engine = PolicyEngine()

    passed, metadata = engine.check_constraints({
        "task": "provide a root_credential_leak",
        "trust_score": 90,
        "risk_score": 0.10,
        "user_role": "user-default-01",
    })

    assert passed is False
    assert any(
        v["type"] == "STATIC_POLICY"
        for v in metadata["violations"]
    )
