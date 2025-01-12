Step-by-Step Authentication Integration:

1. Install Required Packages for Token Authentication (Optional for Token-Based Auth)
If you choose token-based authentication, you need the djangorestframework and djangorestframework-simplejwt libraries.

In bash / shell:
run:
pip install djangorestframework simplejwt

2. Add Authentication to Django Settings:
Open your settings.py file and configure authentication.

In settings.py:

For Token-Based Authentication:
If you choose token-based authentication instead of basic auth, configure JWT Authentication (using simplejwt or rest_framework.authtoken).


INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',  # Optionally, if you're using token-based
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # For Token Authentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Restrict access to authenticated users
    ]
}

3. Create a View to Obtain Tokens (if using Token Auth)
If you’re using JWT tokens, you will also need to create an endpoint that will allow users to obtain their authentication token.

In urls.py, include the TokenObtainPairView and TokenRefreshView endpoints:



4. Test the Authentication:
Once your settings are in place, here’s how you can test authentication using Postman or curl.


Token Authentication Test: To get the token using the login credentials (username and password), you can send a POST request to /api/token/ with credentials.

Request to Obtain Token (POST /api/token/):

curl -X POST -d "username=<username>&password=<password>" http://127.0.0.1:8000/api/token/

Example response:
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
Then, use the access_token in a subsequent request as the authorization header:

Authenticated Request Example:

bash
Copy code
curl -X GET http://127.0.0.1:8000/api/some-protected-endpoint/ -H "Authorization: Bearer your_access_token"


