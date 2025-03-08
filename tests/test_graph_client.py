import pytest
from unittest.mock import patch, MagicMock
from src.graph_client import GraphClient
from helper.logger import logger  # Import the logger

@pytest.fixture(scope="module")
def real_graph_client():
    """Create a real GraphClient instance for testing."""
    client = GraphClient()
    yield client
    client.close()

@pytest.fixture
def mock_graph_client():
    """Create a mock GraphClient instance for testing."""
    with patch('neo4j.GraphDatabase') as mock_driver_class:
        # Set up the mock driver and session
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_transaction = MagicMock()
        
        # Configure the mocks
        mock_driver_class.driver.return_value = mock_driver
        mock_driver.session.return_value.__enter__.return_value = mock_session
        
        # Create a client with the mocked driver
        with patch.object(GraphClient, '__init__', return_value=None):
            client = GraphClient()
            client.driver = mock_driver
            
            yield client, mock_session
            
            # Clean up
            if hasattr(client, 'driver'):
                client.close()

def test_real_execute_query(real_graph_client):
    """Test executing a real query on Neo4j."""

    # First, clean up any existing nodes
    real_graph_client.execute_query("MATCH (n) DETACH DELETE n")

    # Create the first agent
    real_graph_client.execute_query("""
    CREATE (a1:Agent {
        system_message: "You are a psychiatrist.",
        user_message: "Explain bipolar disorder."
    })
    """)

    # Create the second agent
    real_graph_client.execute_query("""
    CREATE (a2:Agent {
        system_message: "You are an accuracy checker.",
        user_message: "Verify the correctness of the psychiatrist's explanation."
    })
    """)

    # Create the third agent
    real_graph_client.execute_query("""
    CREATE (a3:Agent {
        system_message: "You are an evaluator.",
        user_message: "Assess the accuracy checker's feedback and determine its validity and relevance."
    })
    """)

    # Create relationships
    real_graph_client.execute_query("MATCH (a1:Agent {system_message: 'You are a psychiatrist.'}), (a2:Agent {system_message: 'You are an accuracy checker.'}) CREATE (a1)-[:NEXT_AGENT]->(a2)")
    real_graph_client.execute_query("MATCH (a2:Agent {system_message: 'You are an accuracy checker.'}), (a3:Agent {system_message: 'You are an evaluator.'}) CREATE (a2)-[:NEXT_AGENT]->(a3)")

    # Query the test node
    query_result = real_graph_client.execute_query("""
    MATCH (a:Agent {system_message: 'You are a psychiatrist.'}) RETURN a.system_message AS system_message, a.user_message AS user_message
    """)

    # Log the real query response
    logger.info("Real Query Result: %s", query_result)

    # Validate response
    assert isinstance(query_result, list)
    assert len(query_result) > 0
    assert query_result[0]["system_message"] == "You are a psychiatrist."
    assert query_result[0]["user_message"] == "Explain bipolar disorder."

    # Clean up (delete test nodes)
    real_graph_client.execute_query("MATCH (n) DETACH DELETE n")

def test_mock_execute_query(mock_graph_client):
    """Test execute_query with mocked Neo4j session."""
    client, mock_session = mock_graph_client
    
    # Setup mock return value
    mock_record = MagicMock()
    mock_record.data.return_value = {"system_message": "Test message", "user_message": "Test query"}
    mock_session.run.return_value = [mock_record]
    
    # Execute query
    with patch('src.graph_client.logger'):
        result = client.execute_query("MATCH (n) RETURN n", {"param": "value"})
    
    # Assertions
    mock_session.run.assert_called_once_with("MATCH (n) RETURN n", {"param": "value"})
    assert len(result) == 1
    assert result[0]["system_message"] == "Test message"
    assert result[0]["user_message"] == "Test query"

def test_execute_query_with_exception(mock_graph_client):
    """Test execute_query when an exception occurs."""
    client, mock_session = mock_graph_client
    
    # Setup mock to raise exception
    mock_session.run.side_effect = Exception("Test exception")
    
    # Execute query
    with patch('src.graph_client.logger'):
        result = client.execute_query("MATCH (n) RETURN n")
    
    # Assertions
    assert result == []
    mock_session.run.assert_called_once_with("MATCH (n) RETURN n", {})

def test_execute_query_with_empty_result(mock_graph_client):
    """Test execute_query when no results are returned."""
    client, mock_session = mock_graph_client
    
    # Setup mock to return empty result
    mock_session.run.return_value = []
    
    # Execute query
    with patch('src.graph_client.logger'):
        result = client.execute_query("MATCH (n) RETURN n")
    
    # Assertions
    assert result == []
    mock_session.run.assert_called_once_with("MATCH (n) RETURN n", {})
