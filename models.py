from extensions import db,bcrypt,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id  = db.Column(db.Integer(),primary_key = True)
    email = db.Column(db.String(),nullable = False, unique = True)
    username = db.Column(db.String(),nullable = False, unique = True)
    password_hash=db.Column(db.String(length = 60),nullable = False)
    gastos = db.relationship("GestorDeGastosPersonales",backref = "owned_user", lazy = True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)    

class GestorDeGastosPersonales(db.Model):
    id  = db.Column(db.Integer(),primary_key = True)
    descripcion = db.Column(db.String(),nullable = False)
    categoria = db.Column(db.String(),nullable=False)
    monto = db.Column(db.Integer(),default=0)
    fechaDelGasto = db.Column(db.DateTime(),default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))
    def __repr__(self) -> str:
        return f"GestorDeGastosPersonales {self.id}"