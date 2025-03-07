import pytest
from unittest.mock import patch
from src.agent_processor import process_agent

@pytest.fixture
def mock_graph_client():
    """Mock graph_client responses for testing."""
    with patch("src.agent_processor.graph_client") as mock_graph:
        mock_graph.execute_query.side_effect = [
            # First call: Return initial agent's messages
            [{"system_message": "You are a pharmacist", "user_message": "Explain amoxicillin"}],
            # Second call: Return the next agent details
            [{"next_agent_id": 2, "system_message": "You are a critic", "user_message": "Evaluate the explanation"}],
            # Third call: Return the second agent's messages
            [{"system_message": "You are a critic", "user_message": "Evaluate the explanation"}],
            # Fourth call: Return an empty list (end recursion)
            []
        ]
        yield mock_graph

@pytest.fixture
def mock_llm_client():
    """Mock llm_client call_llm responses."""
    with patch("src.agent_processor.llm_client") as mock_llm:
        mock_llm.call_llm.side_effect = [
            {"response": "Amoxicillin is an antibiotic used for bacterial infections."},  # First agent response
            {"response": "The explanation is clear and well-structured."}  # Second agent response
        ]
        yield mock_llm

def test_process_agent(mock_graph_client, mock_llm_client):
    """Test agent processing with mocked graph and LLM clients."""
    node_id = 1
    expected_final_response = "The explanation is clear and well-structured."

    response = process_agent(node_id)

    assert response == expected_final_response, f"Expected '{expected_final_response}', got '{response}'"
