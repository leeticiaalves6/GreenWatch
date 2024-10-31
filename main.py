from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize Flask extensions (database and JWT)
db = SQLAlchemy()
jwt = JWTManager()

# Model definition (simplified for example)
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(80))
    dados = db.Column(db.String(120))

    def json(self):
        return {"id": self.id, "tipo": self.tipo, "dados": self.dados}

# Define the GetAll resource with GET and POST methods
class GetAll(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('tipo')
    argumentos.add_argument('dados')

    def get(self):
        sensors = Sensor.query.all()
        return [sensor.json() for sensor in sensors], 200

    def post(self):
        dados = GetAll.argumentos.parse_args()
        sensor = Sensor(**dados)
        db.session.add(sensor)
        db.session.commit()
        return sensor.json(), 201

# App factory function to create and configure the Flask app
def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sensors.db"  # Use SQLite for local testing
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    jwt.init_app(app)
    
    # Initialize API and add resources
    api = Api(app)
    api.add_resource(GetAll, '/sensor_api')
    
    # Test route to confirm the app is working
    @app.route('/test')
    def test_route():
        return {"status": "working"}, 200

    # Show registered routes for debugging purposes
    with app.app_context():
        db.create_all()  # Creates database tables
        for rule in app.url_map.iter_rules():
            print(f"Registered route: {rule}")

    return app

# Main entry point to run the app
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
