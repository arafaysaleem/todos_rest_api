from flask import Flask, jsonify
from flask_restful import Api
from flask_bcrypt import Bcrypt
from resources.routes import initialize_routes
from flask_jwt_extended import JWTManager

from resources.settings import Settings

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = Settings.JWT_SECRET_KEY
app.config['TRAP_HTTP_EXCEPTIONS']=True

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Error handling
@app.errorhandler(Exception)
def handle_custom_exception(error):
    response = {
        'message': error.message,
        'code': error.code,
        **({'errors': error.payload} if error.payload else {})
    }
    return jsonify(response), error.code

# Map routes to resource classes
initialize_routes(api)

if __name__ == '__main__':
    app.run(port=Settings.PORT)