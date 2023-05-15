from flask import Flask, jsonify
from flask_restful import Api
from resources.routes import initialize_routes
from resources.services import initialize_services

from resources.settings import Settings

app = Flask(__name__)
api = Api(app)
initialize_services(app)

# Error handling
@app.errorhandler(Exception)
def handle_custom_exception(error):
    response = {
        'message': error.message if hasattr(error, 'message') else str('An error occurred'),
        'code': error.code if hasattr(error, 'code') else 500,
    }

    if (hasattr(error, 'payload')):
        response['errors'] = error.payload
    elif (not hasattr(error, 'message')):
        response['message'] = str(error)

    return jsonify(response), response['code']

# Map routes to resource classes
initialize_routes(api)

if __name__ == '__main__':
    app.run(port=Settings.PORT)