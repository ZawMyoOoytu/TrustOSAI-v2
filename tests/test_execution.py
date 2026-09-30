from engines.execution_engine import ExecutionEngine


def test_execution_engine_uses_local_model_by_default(monkeypatch):
    engine = ExecutionEngine()

    def fake_execute(model, task, provider, api_key=None):
        return {
            "response": "test response",
            "quality_score": 0.80,
            "token_telemetry": {
                "prompt_tokens": 3,
                "completion_tokens": 4,
            },
        }

    monkeypatch.setattr(engine.model_router, "execute", fake_execute)

    result = engine.execute(task="hello TrustOSAI")

    assert result["status"] == "COMPLETED"
    assert result["model"] == "local"
    assert result["provider"] == "local"
    assert result["quality_score_qt"] == 0.80
    assert result["token_telemetry"]["total_tokens"] == 7
    assert result["trace"]["engine"] == "ExecutionEngine"


def test_execution_engine_legacy_run(monkeypatch):
    engine = ExecutionEngine()

    def fake_execute(model, task, provider, api_key=None):
        return {
            "response": "hello",
        }

    monkeypatch.setattr(engine.model_router, "execute", fake_execute)

    result = engine.run("test task")

    assert result == "[local] hello"
