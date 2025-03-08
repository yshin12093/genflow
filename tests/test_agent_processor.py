import pytest
from unittest.mock import patch, MagicMock
from src.agent_processor import process_agent, get_agent_messages, get_next_agent

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
    
    # Verify the correct number of calls
    assert mock_graph_client.execute_query.call_count == 4
    assert mock_llm_client.call_llm.call_count == 2

def test_process_agent_with_no_agent_found(mock_graph_client, mock_llm_client):
    """Test process_agent when no agent is found with the given ID."""
    # Override the mock to return empty list for the first call
    mock_graph_client.execute_query.side_effect = [[], None, None, None]
    
    node_id = 999  # Non-existent node ID
    prev_response = "Previous response"
    
    response = process_agent(node_id, prev_response)
    
    # Should return the previous response unchanged
    assert response == prev_response
    assert mock_graph_client.execute_query.call_count == 1
    assert mock_llm_client.call_llm.call_count == 0

def test_process_agent_with_llm_error():
    """Test process_agent when LLM client raises an error."""
    with patch("src.agent_processor.graph_client") as mock_graph:
        mock_graph.execute_query.return_value = [
            {"system_message": "Test system", "user_message": "Test user"}
        ]
        
        with patch("src.agent_processor.llm_client") as mock_llm:
            # Simulate LLM error by returning a response with error
            mock_llm.call_llm.return_value = {"error": "API Error", "statusCode": 500}
            
            response = process_agent("test_id")
            
            # Should handle the error gracefully
            assert "Error processing agent" in response
            assert "API Error" in response

def test_get_agent_messages():
    """Test get_agent_messages function."""
    with patch("src.agent_processor.graph_client") as mock_graph:
        mock_graph.execute_query.return_value = [
            {"system_message": "Test system", "user_message": "Test user"}
        ]
        
        result = get_agent_messages("test_id")
        
        # Verify the query parameters
        mock_graph.execute_query.assert_called_once()
        call_args = mock_graph.execute_query.call_args[0][1]
        assert call_args["node_id"] == "test_id"
        
        # Verify the result
        assert len(result) == 1
        assert result[0]["system_message"] == "Test system"
        assert result[0]["user_message"] == "Test user"

def test_get_next_agent():
    """Test get_next_agent function."""
    with patch("src.agent_processor.graph_client") as mock_graph:
        mock_graph.execute_query.return_value = [
            {"next_agent_id": "next_id", "system_message": "Next system", "user_message": "Next user"}
        ]
        
        result = get_next_agent("current_id")
        
        # Verify the query parameters
        mock_graph.execute_query.assert_called_once()
        call_args = mock_graph.execute_query.call_args[0][1]
        assert call_args["node_id"] == "current_id"
        
        # Verify the result
        assert len(result) == 1
        assert result[0]["next_agent_id"] == "next_id"
