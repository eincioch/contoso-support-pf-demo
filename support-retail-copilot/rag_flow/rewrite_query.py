from promptflow import tool
from promptflow.connections import AzureOpenAIConnection
import os, openai
from jinja2 import Template

@tool
def rewrite_query(query: str, 
                  chat_history: list[str], 
                  customer_data: dict, 
                  azure_open_ai_connection: AzureOpenAIConnection,
                  open_ai_deployment: str) -> str:
    """
    rewrite the query based on the chat history and customer data
    """
    openai.api_type = azure_open_ai_connection.api_type
    openai.api_base = azure_open_ai_connection.api_base
    openai.api_version = azure_open_ai_connection.api_version
    openai.api_key = azure_open_ai_connection.api_key
    jinja_template = os.path.join(os.path.dirname(__file__), "rewrite_query.jinja2")
    with open(jinja_template, encoding="utf-8") as f:
        template = Template(f.read())
    prompt = template.render(query=query, chat_history=chat_history, customer_data=customer_data)
    messages = [
        {
            "role": "system",
            "content": prompt,
        }
    ]

    chat_intent_completion = openai.ChatCompletion.create(
        deployment_id=open_ai_deployment,
        messages=messages,
        temperature=0,
        max_tokens=1024,
        n=1,
    )
    user_intent = chat_intent_completion.choices[0].message.content

    return user_intent