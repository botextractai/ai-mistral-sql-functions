import functools
import json
import sqlite3
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = "REPLACE_THIS_WITH_YOUR_MISTRAL_API_KEY"

model = "mistral-large-latest"

# Define functions
# ================

def retrieve_customer_name(customer_id: str) -> str:
    connection_obj = sqlite3.connect('demo_sqlite.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("SELECT customer_name FROM CUSTOMERS WHERE customer_id = '" + customer_id + "'")
    result = cursor_obj.fetchone()
    cursor_obj.close()
    connection_obj.close()
    if result is not None:
        return json.dumps({"customer_name": result[0]})
    else:
        return json.dumps({"ERROR": "Customer name not found."})

def retrieve_payments_sum(customer_id: str) -> str:
    connection_obj = sqlite3.connect('demo_sqlite.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("SELECT SUM(payment_amount) AS payments_sum FROM PAYMENTS WHERE customer_id = '" + customer_id + "'")
    result = cursor_obj.fetchone()
    cursor_obj.close()
    connection_obj.close()
    if result[0] is not None:
        return json.dumps({"payments_sum":  "${:.2f}".format(result[0])})
    else:
        return json.dumps({"ERROR": "No payments found."})

# Define tools array (JSON Schemas of the tools)
# ==============================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_customer_name",
            "description": "Get customer name from the customer id",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer id.",
                    }
                },
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_payments_sum",
            "description": "Get payments sum from the customer id",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The customer id.",
                    }
                },
                "required": ["customer_id"],
            },
        },
    }
]

# Functools
# =========

names_to_functions = {
    "retrieve_customer_name": functools.partial(retrieve_customer_name),
    "retrieve_payments_sum": functools.partial(retrieve_payments_sum)
}

messages = [
    # Examples of possible questions to start the conversation:
    # "What is my customer name?"
    # "What is the sum of all my payments?"
    ChatMessage(role="user", content="What is the sum of all my payments?")
]

client = MistralClient(api_key=api_key)
response = client.chat(model=model, messages=messages, tools=tools, tool_choice="auto")
print("")
print("****************************************")
print("*** Response from the original query ***")
print("****************************************")
print(response)

messages.append(ChatMessage(role="assistant", content=response.choices[0].message.content))
# Add the user answer "My customer ID is C1003."
messages.append(ChatMessage(role="user", content="My customer ID is C1003."))
response = client.chat(model=model, messages=messages, tools=tools, tool_choice="auto")
print("")
print("******************************************")
print("*** Response with appended customer ID ***")
print("******************************************")
print(response)

messages.append(response.choices[0].message)

# Get function name and params
tool_call = response.choices[0].message.tool_calls[0]
function_name = tool_call.function.name
function_params = json.loads(tool_call.function.arguments)
print("")
print("************************************")
print("*** The function name and params ***")
print("************************************")
print("function_name: ", function_name, "\nfunction_params: ", function_params)

# Execute function
function_result = names_to_functions[function_name](**function_params)
print("")
print("***************************************")
print("*** The result of the function call ***")
print("***************************************")
print(function_result)

# Generate the final answer after appending the function result
messages.append(ChatMessage(role="tool", name=function_name, content=function_result))
response = client.chat(model=model, messages=messages, tools=tools)
print("")
print("************************")
print("*** The final answer ***")
print("************************")
print(response.choices[0].message.content)
