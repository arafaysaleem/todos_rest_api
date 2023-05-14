from .auth import LoginApi, RegisterApi
from .todos import TodosApi, TodoApi

def initialize_routes(api):
 version = 'v1'
 base_url = f'/api/{version}'
 api.add_resource(TodosApi, f'{base_url}/todos/')
 api.add_resource(TodoApi, f'{base_url}/todos/<id>')
 api.add_resource(RegisterApi, f'{base_url}/auth/register')
 api.add_resource(LoginApi, f'{base_url}/auth/login')