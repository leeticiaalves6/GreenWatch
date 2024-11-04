from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

class dbDataModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    umidade = db.Column(db.Float, nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()) 

    def json(self):
        return {
            "id": self.id,
            "umidade": self.umidade,
            "temperatura": self.temperatura,
            "data": self.data.strftime('%Y-%m-%dT%H:%M:%S') if self.data else None
        }

class data_controller(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('umidade')
    argumentos.add_argument('temperatura')

    def get(self):
        data = dbDataModel.query.all()
        return [d.json() for d in data], 200

    def post(self):
        data = data_controller.argumentos.parse_args()
        data = dbDataModel(**data)
        db.session.add(data)
        db.session.commit()
        return data.json(), 201

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sensors.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    jwt.init_app(app)
    
    api = Api(app)
    api.add_resource(data_controller, '/sensor_api')

    with app.app_context():
        db.create_all() 
        for rule in app.url_map.iter_rules():
            print(f"Registered route: {rule}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
