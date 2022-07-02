# Shake IO's currency converter API assessment

## Introduction

This is a currency converter built using FastAPI. It is a simple API that converts one currency to another. It also supports JWT authentication. The system leverages the exchange rates for https://fixer.io

# Usage

-   Clone the repository.
-   Rename .env.example to .env to have access to API keys and some configuration
-   Create a virtual environment and activate it.
-   Install dependencies in the requirements.txt file using `pip install -r requirements.txt`
-   Start the uvicorn server us ing `uvicorn main:app --host 0.0.0.0 --reload`
-   Visit you broswer and check the Swagger docs at `http://127.0.0.1:8000/docs`. This was you have access to all endoints.
-   The system doesn't have any database, so a simple list is used to store user data. On rserver reload, the list is cleared.
-   Make sure you create a new user every time you start the server or make changes to the code.

# Enpoints

-   default
    -   /v1 - Simple return a welcome message
-   auth
    -   /v1/auth/signup - Create a new user
    -   /v1/auth/login - Login a user
    -   /v1/auth/profile - Check details of the currently authenticated user (requires authentication)
-   converter
    -   /v1/converter/currencies - Get a list of available currencies
    -   /v1/converter/latest - Convert one currency to another
    -   /v1/converter/convert - Convert one currency to another (required authentication)
    -   /v1/converter/history - Get a historical rates data based on the date range supplied (requires authentication)

NB: For the 3 endpoints that require authentication. You must make sure you have created a user before you try to access them.
If you are testing on Swagger UI, you can use the Authorize button to login or simply tap the padlock in front of the endpoints that have them. Otherwise, you'll have to call the login endpoint, then use the token generated in the Authorization header in the following format `{"Authorization": "Bearer <token>"}`
 
