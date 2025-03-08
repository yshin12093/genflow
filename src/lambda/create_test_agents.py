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
    """Lambda function to create test agents in Neo4j."""
    try:
        driver = get_neo4j_driver()
        with driver.session() as session:
            # Delete existing nodes
            session.run("MATCH (n) DETACH DELETE n")
            
            # Create agents
            result = session.run("""
            CREATE (a1:Agent {
                system_message: "You are a pharmacist.",
                user_message: "Explain Amoxicillin."
            })
            CREATE (a2:Agent {
                system_message: "You are an accuracy checker.",
                user_message: "Verify the correctness of the pharmacist's explanation."
            })
            CREATE (a3:Agent {
                system_message: "You are an evaluator.",
                user_message: "Assess the accuracy checker's feedback and determine its validity and relevance."
            })
            
            // Create relationships
            CREATE (a1)-[:NEXT_AGENT]->(a2)
            CREATE (a2)-[:NEXT_AGENT]->(a3)
            
            // Return the first agent's ID for testing
            WITH a1
            RETURN elementId(a1) as start_agent_id
            """)
            
            record = result.single()
            start_agent_id = record['start_agent_id']
            
            driver.close()
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'start_agent_id': start_agent_id
                })
            }
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
