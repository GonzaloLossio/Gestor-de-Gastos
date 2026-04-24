from flask import request,redirect,render_template,flash,jsonify
from extensions import db
from models import GestorDeGastosPersonales
from . import routes_bp
from forms import Registro,Login
from models import User
from flask_login import login_user,logout_user,current_user

@routes_bp.route('/register',methods=["POST","GET"])
def registerPage():
    form = Registro()
    if form.validate_on_submit():
        usuarioACrear = User(username = form.username.data,email = form.email_adress.data,password = form.password1.data)
        try:
            db.session.add(usuarioACrear)
            db.session.commit()
            flash(f"Te has registrado Correctamente!", category="success")
            return redirect ("/")
        except Exception as e:
            return f"ERROR: {e}"
        
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Hubo un error al momento de crear el usuario: {err_msg}',category="danger")
    else:
        return render_template("register.html",form=form)


#database page
@routes_bp.route('/gastos',methods =["POST","GET"])
def gastos():
    if request.method == "POST":
        data = request.get_json()

        descripcion_actual = data.get('descripcion')
        categoria_actual = data.get('categoria')
        monto_actual =  data.get('monto')

        gasto = GestorDeGastosPersonales(descripcion=descripcion_actual,categoria=categoria_actual,monto=monto_actual,owner=current_user.id) 
    
        try:
            db.session.add(gasto)
            db.session.commit()
            return jsonify({"status" : "success","gasto":{
                "id": gasto.id, "descripcion" : gasto.descripcion,"categoria": gasto.categoria, "monto" : gasto.monto, "fecha":gasto.fechaDelGasto.strftime("%d-%m-%Y")
            }})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        gastoss = GestorDeGastosPersonales.query.filter_by(owner=current_user.id).order_by(GestorDeGastosPersonales.fechaDelGasto).all() 
        return render_template("index.html",gastos=gastoss)
    
#delete
@routes_bp.route("/delete/<int:id>",methods = ['POST'])
def deletebutton(id:int):
    gastoAEliminar = GestorDeGastosPersonales.query.get_or_404(id)
    if gastoAEliminar.owner != current_user.id:
        return "No autorizado",403
    try:
        db.session.delete(gastoAEliminar)
        db.session.commit()

        return jsonify({"status":"success","message": "Gasto Eliminado"})
    
    except Exception as e:
        return f"ERROR: {e}"
    
#edit
@routes_bp.route("/edit/<int:id>",methods =["POST","GET"])
def edit(id:int):
    gastoEditar = GestorDeGastosPersonales.query.get_or_404(id)
    if request.method == "POST":
        gastoEditar.descripcion = request.form['descripcion']
        gastoEditar.categoria = request.form['categoria']
        gastoEditar.monto = request.form['monto']

        if gastoEditar.owner != current_user.id:
            return "No autorizado",403
    
        try:
            db.session.commit()
            return redirect("/gastos")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template("edit.html",gasto = gastoEditar)
    

@routes_bp.route("/",methods = ["POST","GET"])
def login():
    form = Login()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email_adress.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Has accedido como: {attempted_user.username}",category="succes")
            return redirect("/gastos")
        else:
            flash(f"El email o la contraseaña no coinciden, prueba denuevo!",category="danger")
    return render_template("home.html",form=form)

@routes_bp.route("/logout")
def logout():
    logout_user()
    flash(f"Has finalizado la sesion",category="succes")
    return redirect ("/")