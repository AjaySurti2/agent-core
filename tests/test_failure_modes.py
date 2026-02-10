from agent_core.core.llm_planner import LLMPlanner


def test_unable_to_plan_guardrail():
    planner = LLMPlanner()

    # Provide a state that forces planner to NOT take action
    result = planner.plan({"task_count": 10})

    assert isinstance(result, dict)
    assert result["action"] == "idle"


