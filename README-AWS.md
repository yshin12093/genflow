# AWS Step Functions Migration Guide

This guide explains how to deploy the agent processing workflow to AWS Step Functions and Lambda.

## Architecture Overview

The agent processing workflow has been split into three Lambda functions:
1. `get_agent_messages` - Fetches agent messages from Neo4j
2. `get_next_agent` - Finds the next agent in the sequence
3. `process_agent` - Processes the agent request using the configured LLM

These functions are orchestrated by an AWS Step Functions state machine defined in `step_functions/agent_workflow.asl.json`.

## Required AWS Resources

1. Three Lambda functions with Python 3.9+ runtime
2. Step Functions state machine
3. IAM roles with appropriate permissions
4. Environment variables for configuration

## Environment Variables

Each Lambda function requires the following environment variables:

### Neo4j Connection (get_agent_messages.py, get_next_agent.py)
- NEO4J_URI
- NEO4J_USER
- NEO4J_PASSWORD

### LLM Configuration (process_agent.py)
- LLM_PROVIDER (one of: 'deepseek', 'openai', 'anthropic')
- DEEPSEEK_API_KEY (if using DeepSeek)
- OPENAI_API_KEY (if using OpenAI)
- CLAUDE_API_KEY (if using Claude)

## Deployment Steps

1. Create Lambda functions:
   ```bash
   # Install dependencies to a local directory
   pip install -r requirements-lambda.txt -t lambda_layer/python

   # Create a ZIP file for the Lambda layer
   cd lambda_layer && zip -r ../lambda_layer.zip . && cd ..

   # Create ZIP files for each Lambda function
   zip get_agent_messages.zip src/lambda/get_agent_messages.py
   zip get_next_agent.zip src/lambda/get_next_agent.py
   zip process_agent.zip src/lambda/process_agent.py
   ```

2. Create the Step Functions state machine:
   - Replace the `${FunctionName}` placeholders in `agent_workflow.asl.json` with the actual Lambda ARNs
   - Create a new state machine using the AWS Console or CLI

3. Update IAM roles:
   - Lambda execution roles need permissions for CloudWatch Logs
   - Step Functions execution role needs permissions to invoke Lambda functions

## Usage

To start the workflow, invoke the Step Functions state machine with the following input:

```json
{
  "node_id": "your-agent-node-id",
  "prev_response": "" // Optional
}
```

The workflow will process the agent chain and return the final response.
