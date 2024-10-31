from flask_restful import Resource, reqparse
from app.models import Sensor
from app import db

class GetAll(Resource):
    
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('tipo')
    argumentos.add_argument('dados')
    
    def get(self):
        return 200
        sensors = Sensor.query.all()
        return [sensor.json() for sensor in sensors], 200
    
    def post(self):            
        dados = GetAll.argumentos.parse_args()
        sensor = Sensor(**dados)
        db.session.add(sensor)
        db.session.commit()     
        return sensor.json(), 201      
