from flask import Flask, jsonify
from models import set_db, Plant
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    # resources = specific domains to access / allow cros origin for specific routes
    CORS(app , resources = {r"*/api/*": {"origins": "*"}} ) #first element specifcies what resource we talking about - what origins from the client can access those resources from that type of api, the * anything can come before or after / api of the uri resource - and that any origin can access that end point
    
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers' , 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
@app.route('/')
@cross_origin() #allows for cross origin for endpoint
def hello():
    return jsonify({'message': 'Hello World'})

@app.route("/hello", methods=['GET', 'POST'])
@cross_origin()
def get_greeting():
    if request.method == 'POST':
        return create_greeting()
    else:
        page = request.args.get('page', 1, type=int)
        return send_greeting()
    
    
    
    