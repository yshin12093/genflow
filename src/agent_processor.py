import json
import os
import sys
from helper.logger import logger  # Import centralized logger

# Ensure the project root is added to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# Import graph and LLM clients using absolute paths
from src.graph_client import graph_client
from src.llm_client import llm_client

def get_agent_messages(node_id: str) -> list[dict]:
    """Fetch agent's messages from the graph database."""
    query = """
    MATCH (a:Agent) 
    WHERE elementId(a) = $node_id
    RETURN a.system_message AS system_message, a.user_message AS user_message
    """
    return graph_client.execute_query(query, {"node_id": node_id})

def get_next_agent(node_id: str) -> list[dict]:
    """Find the next agent in sequence."""
    query = """
    MATCH (a:Agent)-[:NEXT_AGENT]->(next:Agent)
    WHERE elementId(a) = $node_id
    RETURN elementId(next) AS next_agent_id, next.system_message AS system_message, next.user_message AS user_message
    """
    return graph_client.execute_query(query, {"node_id": node_id})

def process_agent(node_id: str, prev_response: str = "") -> str:
    """Recursive function to process agents."""
    
    agent_data = get_agent_messages(node_id)

    if not agent_data:
        logger.warning(f"❌ No agent found with node_id {node_id}")
        return prev_response

    system_message = agent_data[0].get('system_message', 'No system message found')
    user_message = agent_data[0].get('user_message', 'No user message found')

    full_message = user_message + " " + prev_response

    response_dict = llm_client.call_llm(system_message, full_message)
    
    # Check if there's an error in the response
    if "error" in response_dict:
        error_msg = f"LLM API Error: {response_dict.get('error')}"
        logger.error(f"❌ {error_msg}")
        return f"Error processing agent: {error_msg}"
    
    response = response_dict.get("response", "No response found")
    logger.info(f"✅ Agent (ID {node_id}) Response: {response}")

    next_agent_data = get_next_agent(node_id)

    if next_agent_data:
        next_node_id = next_agent_data[0].get('next_agent_id', None)
        return process_agent(next_node_id, response)
    
    logger.info("✅ Reached the last agent.")
    return response
