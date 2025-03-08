import json
import os
from neo4j import GraphDatabase

def get_neo4j_driver():
    uri = os.environ['NEO4J_URI']
    user = os.environ['NEO4J_USER']
    password = os.environ['NEO4J_PASSWORD']
    return GraphDatabase.driver(uri, auth=(user, password))

def lambda_handler(event, context):
    """Lambda function to fetch agent's messages from Neo4j."""
    try:
        node_id = event['node_id']
        
        driver = get_neo4j_driver()
        with driver.session() as session:
            query = """
            MATCH (a:Agent) 
            WHERE elementId(a) = $node_id
            RETURN a.system_message AS system_message, a.user_message AS user_message
            """
            result = session.run(query, {"node_id": node_id}).single()
            driver.close()
            
            if not result:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': f'No agent found with node_id {node_id}'})
                }
            
            # Return the data in the exact format expected by process_agent
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'system_message': result['system_message'],
                    'user_message': result['user_message']
                })
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
