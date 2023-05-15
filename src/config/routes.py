
from ..controllers.auth_controller import LoginController, RegisterController
from ..controllers.todos_controller import TodoController, TodosController

def initialize_routes(api):
 version = 'v1'
 base_url = f'/api/{version}'
 api.add_resource(TodosController, f'{base_url}/todos/')
 api.add_resource(TodoController, f'{base_url}/todos/<id>')
 api.add_resource(RegisterController, f'{base_url}/auth/register')
 api.add_resource(LoginController, f'{base_url}/auth/login')