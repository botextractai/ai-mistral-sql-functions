# Mistral Large Language Model (LLM) function calling with SQL queries

Mistral offers multiple Large Language Models (LLMs). Some of them have native fluency in English, French, Spanish, German, and Italian. These multi-lingual LLMs can be used in any of these languages.

Function calling allows Mistral models to connect to external tools. By integrating Mistral models with external tools such as user defined functions or APIs, users can easily build applications catering to specific use cases and practical problems.

This example works with the [Mistral Large](https://mistral.ai/technology/#models) Large Language Model (LLM). However, you can also use other Mistral models that have been trained to handle function calls.

You need a Mistral API key for this project. [Get your Mistral API key here](https://auth.mistral.ai/ui/registration). Insert your Mistral API key in the `mistral.py` script.

This example contains two tools for retrieving the customer name and the sum of all payments for a given customer ID from a sqlite SQL database.

The model automatically chooses the right tool to answer the question, because we outline the function specifications with a JSON schema, so that the model can understand it. Specifically, we describe the type, function name, function description, function parameters, and the required parameter for each of the two functions in an array that contains both JSON schemas. We then organise the two functions into a dictionary where keys represent the function name, and values are the function. This allows us to call each function based on its function name.

The sqlite database `demo_sqlite.db` can be created with the `db_create-py` script. The database contains two tables ("CUSTOMERS" and "PAYMENTS") with this data:

"CUSTOMERS" table
```
| customer_id | customer_name |
| ----------- | ------------- |
| C1001       | Smith         |
| C1002       | Johnson       |
| C1003       | Williams      |
| C1004       | Brown         |
| C1005       | Jones         |
```

"PAYMENTS" table
```
| customer_id | payment_amount |
| ----------- | -------------- |
| C1001       | 10.85          |
| C1002       | 23.41          |
| C1003       | 19.62          |
| C1004       | 48.17          |
| C1005       | 11.94          |
| C1001       | 34.29          |
| C1002       | 27.43          |
| C1003       | 44.98          |
| C1004       | 16.75          |
| C1005       | 30.12          |
```

The script `mistral.py` follows this flow:

1. The user asks the question "What is the sum of all my payments?"
2. The model automatically finds the correct tool and determines that it needs the customer ID as input parameter for the tool. It therefore asks the user: "To provide you with the sum of all your payments, I would need your customer ID. Could you please provide it?"
3. The user answers with "My customer ID is C1003."
4. Get the function name and parameters.
5. Execute the function.
6. The model provides the answer using its natural language capabilities.

Note: Currently, it is the user's responsibility to execute functions. In the future, Mistral might introduce helpful functions that can be executed server-side.

## Some example questions

| Expected Function      | Question                                |
| ---------------------- | --------------------------------------- |
| retrieve_customer_name | `"What is my customer name?"`           |
| retrieve_payments_sum  | `"What is the sum of all my payments?"` |
