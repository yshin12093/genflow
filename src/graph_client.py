from neo4j import GraphDatabase
from config import GRAPH_DB_TYPE, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from helper.logger import logger  # Import the logger

class GraphClient:
    """Unified interface for interacting with Neo4j graph database."""

    def __init__(self) -> None:
        """Initialize the database connection based on the configured provider."""
        if GRAPH_DB_TYPE.lower() == "neo4j":
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            logger.info("✅ Connected to Neo4j")  # Log successful connection
        else:
            logger.error(f"❌ Unsupported GRAPH_DB_TYPE: {GRAPH_DB_TYPE}")
            raise ValueError(f"❌ Unsupported GRAPH_DB_TYPE: {GRAPH_DB_TYPE}")

    def close(self) -> None:
        """Close the database connection."""
        if hasattr(self, "driver"):
            self.driver.close()
            logger.info("✅ Closed Neo4j connection")

    def execute_query(self, query: str, parameters: dict = None) -> list[dict]:
        """Execute a Cypher query and return the results."""
        try:
            with self.driver.session() as session:
                result = [record.data() for record in session.run(query, parameters or {})]
                logger.info(f"✅ Executed Query: {query}")  # Log query execution
                return result
        except Exception as e:
            logger.error(f"❌ Query Execution Failed: {e}")
            return []

# Create a singleton instance
graph_client = GraphClient()
