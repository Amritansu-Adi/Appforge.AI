"""
ai-service/tests/test_overview_chain.py
Owner: Prateeksha
Status: STUB — implement in Phase 2.3 alongside overview_chain

Run: pytest ai-service/tests/test_overview_chain.py
"""
import pytest

@pytest.mark.asyncio
async def test_overview_chain_returns_all_fields():
    """Chain must return OverviewOutput with all 7 fields populated."""
    # TODO Phase 2.3 (Prateeksha):
    # from ai_service.chains.overview_chain import overview_chain
    # from ai_service.parsers.overview_parser import overview_parser
    # Replace llm with llm_mock before invoking
    pytest.skip("Implement in Phase 2.3")

@pytest.mark.asyncio
async def test_overview_chain_handles_fenced_json():
    """PydanticOutputParser must still succeed even if LLM wraps JSON in ```json fences."""
    pytest.skip("Implement in Phase 2.3")
