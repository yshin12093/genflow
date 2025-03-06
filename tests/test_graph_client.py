import pytest
from src.graph_client import GraphClient
from helper.logger import logger  # ✅ Import the logger

@pytest.fixture(scope="module")
def real_graph_client():
    """Create a real GraphClient instance for testing."""
    client = GraphClient()
    yield client
    client.close()

def test_real_execute_query(real_graph_client):
    """Test executing a real query on Neo4j."""
    
    # ✅ Insert a test node
    real_graph_client.execute_query("""
    MERGE (a:Agent {system_message: 'Test Agent', user_message: 'Hello World'})
    RETURN a
    """)

    # ✅ Query the test node
    query_result = real_graph_client.execute_query("""
    MATCH (a:Agent {system_message: 'You are a pharmacist'}) RETURN a.system_message AS system_message, a.user_message AS user_message
    """)

    # ✅ Log the real query response
    logger.info("✅ Real Query Result: %s", query_result)

    # ✅ Validate response
    assert isinstance(query_result, list)
    assert len(query_result) > 0
    assert query_result[0]["system_message"] == "You are a pharmacist"
    assert query_result[0]["user_message"] == "Explain amoxicillin"

    # ✅ Clean up (delete test node)
    real_graph_client.execute_query("""
    MATCH (a:Agent {system_message: 'Test Agent'}) DELETE a
    """)
