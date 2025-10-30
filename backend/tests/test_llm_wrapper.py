import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.ai import llm_client

def test_llm_response_parsing(monkeypatch):
    # Fake LLM output with structured JSON
    fake_output = """
    {
      "top_categories": [{"category": "Food", "total": 200}],
      "advice": "Spend less on fast food.",
      "summary": "Food is your top category."
    }
    """

    # Mock generate() to return our fake output
    monkeypatch.setattr(llm_client.LLMClient, "generate", lambda self, prompt: fake_output)

    transactions = [{"category": "Food", "amount": 10}, {"category": "Bills", "amount": 20}]
    result = llm_client.analyze_transactions_with_llm(transactions)
    
    assert "top_categories" in result
    assert isinstance(result["top_categories"], list)
    assert "advice" in result
    assert "summary" in result
