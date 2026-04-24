


from flask import Flask
from flask_scss import Scss
from extensions import db,bcrypt,login_manager

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///GestorDeGastosPersonales.db"
app.config['SECRET_KEY'] = '24c089ed4399a2bc19916bc9'
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
Scss(app)

from routes import routes_bp
app.register_blueprint(routes_bp)

if __name__ in '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)