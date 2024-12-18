from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recetas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    pasos = db.Column(db.Text, nullable=False)

def iniciar_db():
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    recetas = Receta.query.all()
    return render_template('index.html', recetas=recetas)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_receta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ingredientes = request.form['ingredientes']
        pasos = request.form['pasos']

        if not nombre or not ingredientes or not pasos:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('agregar_receta'))

        nueva_receta = Receta(nombre=nombre, ingredientes=ingredientes, pasos=pasos)
        db.session.add(nueva_receta)
        db.session.commit()
        flash('Receta agregada exitosamente.', 'success')
        return redirect(url_for('home'))

    return render_template('agregar.html')

@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar_receta(id):
    receta = Receta.query.get_or_404(id)
    if request.method == 'POST':
        receta.nombre = request.form['nombre'] or receta.nombre
        receta.ingredientes = request.form['ingredientes'] or receta.ingredientes
        receta.pasos = request.form['pasos'] or receta.pasos

        db.session.commit()
        flash('Receta actualizada exitosamente.', 'success')
        return redirect(url_for('home'))

    return render_template('actualizar.html', receta=receta)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    db.session.delete(receta)
    db.session.commit()
    flash('Receta eliminada exitosamente.', 'success')
    return redirect(url_for('home'))

if __name__ == "__main__":
    iniciar_db()
    app.run(debug=True)
