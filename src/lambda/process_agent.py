import os
import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        node_id = event.get('node_id')
        agent_data = event.get('agent_data', {})
        prev_response = event.get('prev_response', '')

        logger.info(f"Processing agent_data: {json.dumps(agent_data)}")

        system_message = agent_data.get('system_message', '')
        user_message = agent_data.get('user_message', '')

        if not system_message or not user_message:
            error_msg = 'Missing system_message or user_message in agent_data'
            logger.error(error_msg)
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': error_msg
                })
            }

        # Construct the messages for the LLM
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message}
        ]

        if prev_response:
            messages.append({'role': 'assistant', 'content': prev_response})

        logger.info(f"Constructed messages: {json.dumps(messages)}")

        # Get the LLM provider and API key
        llm_provider = os.environ.get('LLM_PROVIDER', '').lower()
        logger.info(f"Using LLM provider: {llm_provider}")
        
        api_response = None

        if llm_provider == 'deepseek':
            api_key = os.environ.get('DEEPSEEK_API_KEY')
            if not api_key:
                error_msg = 'DEEPSEEK_API_KEY not configured'
                logger.error(error_msg)
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': error_msg
                    })
                }

            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'deepseek-chat',
                    'messages': messages,
                    'temperature': 0.7,
                    'max_tokens': 1000
                }
            )
            api_response = response.json()
            logger.info(f"Deepseek API response: {json.dumps(api_response)}")
            response_text = api_response.get('choices', [{}])[0].get('message', {}).get('content', '')

        elif llm_provider == 'openai':
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                error_msg = 'OPENAI_API_KEY not configured'
                logger.error(error_msg)
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': error_msg
                    })
                }

            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': messages,
                    'temperature': 0.7,
                    'max_tokens': 1000
                }
            )
            api_response = response.json()
            logger.info(f"OpenAI API response: {json.dumps(api_response)}")
            response_text = api_response.get('choices', [{}])[0].get('message', {}).get('content', '')

        elif llm_provider == 'claude':
            api_key = os.environ.get('CLAUDE_API_KEY')
            if not api_key:
                error_msg = 'CLAUDE_API_KEY not configured'
                logger.error(error_msg)
                return {
                    'statusCode': 500,
                    'body': json.dumps({
                        'error': error_msg
                    })
                }

            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'claude-3-opus-20240229',
                    'messages': messages,
                    'max_tokens': 1000,
                    'temperature': 0.7
                }
            )
            api_response = response.json()
            logger.info(f"Claude API response: {json.dumps(api_response)}")
            response_text = api_response.get('content', [{}])[0].get('text', '')

        else:
            error_msg = f'Unsupported LLM provider: {llm_provider}'
            logger.error(error_msg)
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': error_msg
                })
            }

        logger.info(f"Final response: {response_text}")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': response_text,
                'node_id': node_id
            })
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
