![Simple API Management Logo](https://storage.googleapis.com/simple-api-management-assets/logo.svg) 
# Simple API Management Python WSGI based Frameworks Middleware

## Installation

```bash
$ pip install simple-api-management-wsgi
```

## Usage

```python
def identifier(environ, app):
    return environ['REMOTE_ADDR']

simple_api_management_options = {
    'KEY': 'add your key here',
    'IDENTIFIER': identifier #optional
}

app.wsgi_app = SimpleAPIManagementMiddleware(app.wsgi_app, simple_api_management_options)
```
