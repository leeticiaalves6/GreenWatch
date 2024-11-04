# from app import db

# class Sensor(db.Model):
#     __tablename__ = "sensor"
#     id = db.Column(db.Integer, primary_key=True)
#     tipo = db.Column(db.String(255), nullable=False)
#     dados = db.Column(db.String(255), nullable=False)
#     data = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()) 
#     def json(self):
#         return{
#             'id':self.id,
#             'tipo':self.tipo,
#             'dados':self.dados                                         
#         }    
