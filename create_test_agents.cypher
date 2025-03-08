// Delete all existing nodes and relationships
MATCH (n) DETACH DELETE n;

// Create agents
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
MATCH (a:Agent)
WHERE NOT ()-[:NEXT_AGENT]->(a)
RETURN elementId(a) as start_agent_id;

COMMIT;
