import json
import os
from neo4j import GraphDatabase
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_neo4j_driver():
    uri = os.environ['NEO4J_URI']
    user = os.environ['NEO4J_USER']
    password = os.environ['NEO4J_PASSWORD']
    return GraphDatabase.driver(uri, auth=(user, password))

def lambda_handler(event, context):
    """Lambda function to get the next agent in sequence from Neo4j."""
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        node_id = event['node_id']
        logger.info(f"Looking for next agent after node_id: {node_id}")
        
        driver = get_neo4j_driver()
        with driver.session() as session:
            query = """
            MATCH (current:Agent)-[:NEXT_AGENT]->(next:Agent)
            WHERE elementId(current) = $node_id
            RETURN elementId(next) as next_agent_id
            """
            result = session.run(query, {"node_id": node_id}).single()
            driver.close()
            
            if not result:
                logger.info(f"No next agent found for node_id: {node_id}")
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': f'No next agent found for node_id {node_id}'})
                }
            
            next_agent_id = result['next_agent_id']
            logger.info(f"Found next agent with id: {next_agent_id}")
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'next_agent_id': next_agent_id
                })
            }
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
