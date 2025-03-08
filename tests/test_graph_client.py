import pytest
from src.graph_client import GraphClient
from helper.logger import logger  # Import the logger

@pytest.fixture(scope="module")
def real_graph_client():
    """Create a real GraphClient instance for testing."""
    client = GraphClient()
    yield client
    client.close()

def test_real_execute_query(real_graph_client):
    """Test executing a real query on Neo4j."""

    # Graph creation query
    creation_query = '''

    // Delete all existing nodes and relationships
    MATCH (n) DETACH DELETE n;

    // Create agents
    CREATE (a1:Agent {
        system_message: "You are a psychiatrist.",
        user_message: "Explain bipolar disorder."
    })
    CREATE (a2:Agent {
        system_message: "You are an accuracy checker.",
        user_message: "Verify the correctness of the psychiatrist's explanation."
    })
    CREATE (a3:Agent {
        system_message: "You are an evaluator.",
        user_message: "Assess the accuracy checker's feedback and determine its validity and relevance."
    })

    // Create relationships
    CREATE (a1)-[:NEXT_AGENT]->(a2)
    CREATE (a2)-[:NEXT_AGENT]->(a3)
    '''
    real_graph_client.execute_query(creation_query)

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
    real_graph_client.execute_query("""
    MATCH (n) DETACH DELETE n;
    """)
